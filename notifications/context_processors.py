from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from notifications.models import Notification

User = get_user_model()


def notifications_count(request):
    """
    Custom context processor for notifications count.
    """
    count_notifications = 0
    # check if current user is authenticated or not.
    if request.user.is_authenticated:
        # get current user 
        user = get_object_or_404(User, id=request.user.id)
        # get user notifications count
        count_notifications = Notification.objects.notifications_count(user)
    return {'count_notifications':count_notifications}     