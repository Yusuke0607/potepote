from .models import UserNotification,Notification

def notifications(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.order_by('-created_at').all()
        read_notification_ids = UserNotification.objects.filter(user=request.user, is_read=True).values_list('notification_id', flat=True)
        unread_notifications = [notification for notification in notifications if notification.id not in read_notification_ids]
        read_notifications = Notification.objects.filter(id__in=read_notification_ids).order_by('-created_at')
        return {'unread_notifications': unread_notifications, 'read_notifications': read_notifications}
    return {}
