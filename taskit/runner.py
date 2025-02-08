import uuid
from importlib import import_module
from concurrent.futures import ThreadPoolExecutor
from jestit.helpers import redis
from objict import objict
import metrics


class TaskEngine:
    def __init__(self, channels, max_workers=5, task_expiration=3600):
        self.redis = redis.get_connection()
        self.channels = channels
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.task_expiration = task_expiration
        self.reinitialize_pending_tasks()

    def get_pending_key(self, channel):
        return f"taskit:p:{channel}"

    def get_error_key(self, channel):
        return f"taskit:e:{channel}"

    def get_running_key(self, channel):
        return f"taskit:r:{channel}"

    def get_task_key(self, task_id):
        return f"taskit:t:{task_id}"

    def get_task_data(self, task_id):
        task_data_raw = self.redis.get(self.get_task_key(task_id))
        return objict.from_json(task_data_raw, ignore_errors=True)

    def reinitialize_pending_tasks(self):
        for channel in self.channels:
            # we need to rerun any tasks stuck in running
            running_tasks = self.redis.smembers(self.get_running_key(channel))
            for task_id in running_tasks:
                self.redis.sadd(self.get_pending_key(channel), task_id)
                self.redis.srem(self.get_running_key(channel), task_id)
                self.add_task(task_id)
            pending_tasks = self.redis.smembers(self.get_pending_key(channel))
            for task_id in pending_tasks:
                self.add_task(task_id)

    def handle_message(self, message):
        self.add_task(message['data'].decode())

    def on_run_task(self, task_id):
        task_key = self.get_task_key(task_id)
        task_data = self.get_task_data(task_id)
        function_path = task_data.get('function')
        module_name, func_name = function_path.rsplit('.', 1)
        module = import_module(module_name)
        func = getattr(module, func_name)
        self.redis.srem(self.get_pending_key(task_data.channel), task_id)
        self.redis.sadd(self.get_running_key(task_data.channel), task_id)
        try:
            func(task_data)
            self.redis.delete(task_key)
            metrics.record_metrics("taskit:d:global", category="taskit")
            metrics.record_metrics(f"taskit:d:{task_data.channel}", category="taskit_channels")
        except Exception as e:
            self.redis.sadd(self.get_error_key(task_data.channel), task_id)
            self.redis.set(f"taskit:err:{task_id}", str(e), ex=3600)
            metrics.record_metrics("taskit:e:global", category="taskit")
            metrics.record_metrics(f"taskit:e:{task_data.channel}", category="taskit_channels")

        finally:
            self.redis.srem(self.get_running_key(task_data.channel), task_id)

    def add_task(self, task_id):
        self.executor.submit(self.on_run_task, task_id)

    def start_listening(self):
        pubsub = self.redis.pubsub()
        pubsub.subscribe(**{channel: self.handle_message for channel in self.channels})
        for message in pubsub.listen():
            if message['type'] != 'message':
                continue
            self.handle_message(message)


# HELPERS FOR RUNNING VIA CLI
def setup_parser():
    import argparse
    parser = argparse.ArgumentParser(description="Task Engine")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Enable verbose logging")
    return parser.parse_args()


def main():
    from jestit.helpers.settings import settings
    engine = TaskEngine(settings.TASKIT_CHANNELS)
    engine.start_listening()

if __name__ == "__main__":
    opts = setup_parser()
    main()
