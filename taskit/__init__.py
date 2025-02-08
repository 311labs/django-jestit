from jestit.helpers import redis
from objict import objict
import uuid
import time
import metrics


def publish_task(channel, function, data, expires=1800):
    redis_con = redis.get_connection()
    task_data = objict(channel=channel, function=function, data=objict.from_dict(data))
    task_data.id = str(uuid.uuid4()).replace('-', '')
    task_data.created = time.time()
    channel_key = f"taskit:c:{channel}"
    task_key = f"taskit:t:{task_data.id}"
    pending_key = f"taskit:p:{channel}"
    redis_con.sadd(pending_key, task_data.id)
    redis_con.set(task_key, task_data.to_json(as_string=True), ex=expires)
    redis_con.publish(channel_key, task_data.id)
    metrics.record_metrics("taskit:p:global", category="taskit")
    metrics.record_metrics(f"taskit:p:{channel}", category="taskit_channels")


def get_status(self, channels):
    status = objict(pending=0, running=0, channels=objict())
    redis_con = redis.get_connection()
    for channel in channels:
        running_key = f"taskit:r:{channel}"
        pending_key = f"taskit:p:{channel}"
        status.channels[channel] = objict()
        status.channels[channel].pending = list(redis_con.smembers(pending_key))
        status.channels[channel].running = list(redis_con.smembers(running_key))
        status.pending += len(status.channels[channel].pending)
        status.running += len(status.channels[channel].running)
    return status
