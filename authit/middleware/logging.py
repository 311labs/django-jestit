from jestit.helpers import logit

logger = logit.get_logger("requests", "requests.log")

class LoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only log if the endpoint starts with '/api'
        if request.path.startswith('/api'):
            # Log Request details with data
            logger.info(
                "REQUEST",
                f"{request.META.get('REMOTE_ADDR', '')} - {request.path}",
                request.GET,
                request.body
            )
        response = self.get_response(request)
        # Only log if the endpoint starts with '/api'
        if request.path.startswith('/api'):
            # Log Response details with data
            logger.info(
                "RESPONSE",
                f"{request.META.get('REMOTE_ADDR', '')} - {request.path}",
                response.content
            )
        return response
