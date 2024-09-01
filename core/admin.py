from django.contrib import admin
from .models import AccessLog

@admin.register(AccessLog)
class AccessLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'timestamp', 'details')
    list_filter = ('user', 'action', 'timestamp')
    search_fields = ('action', 'details')
    readonly_fields = ('user', 'action', 'timestamp', 'details')

    verbose_name = 'システムアクセスログ'
    verbose_name_plural = 'システムアクセスログ一覧'
