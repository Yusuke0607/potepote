from django.shortcuts import redirect
from functools import wraps

from .models import AccessLog

def log_access(user, action, details=''):
    AccessLog.objects.create(user=user, action=action, details=details)
