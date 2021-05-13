from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class NotificationManager(models.Manager):
    """
    Override the Notification manager.
    """
    def notifications_received(self, receiver):
        """
        Take a receiver, and return all his received notifications.
        """
        return Notification.objects.filter(receiver=receiver, is_active=True).exclude(sender=receiver)

    def notifications_count(self, receiver):
        """
        Take a receiver, and count his notifications.
        """
        return Notification.objects.filter(receiver=receiver, 
                            is_seen=False, is_active=True).exclude(sender=receiver).count()    

    def notifications_updated(self, receiver):
        """
        Take a receiver, and update his notifications after seeing them.
        """
        return Notification.objects.filter(receiver=receiver, is_seen=False).update(is_seen=True)

    def set_inactive(self, sender, receiver, notification_type, post=None, comment=None):
        """
        Take sender, receiver, notification_type, post, and comment.
        Set the notification to be inactive.
        """
        if post:
            return Notification.objects.filter(sender=sender, receiver=receiver, post=post,
                notification_type=notification_type, is_active=True).update(is_active=False)
        elif comment:
            return Notification.objects.filter(sender=sender, receiver=receiver, comment=comment,
                notification_type=notification_type, is_active=True).update(is_active=False)        
        else:
            return Notification.objects.filter(sender=sender, receiver=receiver, 
                notification_type=notification_type, is_active=True).update(is_active=False)


class Notification(models.Model):
    """
    Notification model.
    """
    NOTIFICATION_TYPE = (
        ('like', 'like'),
        ('comment', 'comment'),
        ('comment_like', 'comment like'),
    )

    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='noti_from_user')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='noti_to_user')
    post = models.ForeignKey("posts.Post", on_delete=models.CASCADE, related_name='noti_post', blank=True, null=True)
    comment = models.ForeignKey("posts.Comment", on_delete=models.CASCADE, related_name='noti_comment', blank=True, null=True)
    notification_type = models.CharField(max_length=14, choices=NOTIFICATION_TYPE)
    is_seen = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
   
    objects = NotificationManager()
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        # Return sender's username, receiver's username, and the notification type.
        return f'{self.sender}-{self.receiver}-{self.notification_type}'