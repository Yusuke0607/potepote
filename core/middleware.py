from django.utils.timezone import now
from .utils import log_access

class AccessLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.user.is_authenticated:
            log_access(request.user, request.path)
        return response
