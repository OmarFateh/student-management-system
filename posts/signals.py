from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save

from notifications.models import Notification
from .models import Post, Comment
from adminhod.utils import unique_slug_generator


@receiver(pre_save, sender=Post)     # receiver(signal, **kwargs) # to register a signal
def create_post_slug(sender, instance, *args, **kwargs):
    """
    Create a slug for an post before saving.
    """
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

@receiver(post_save, sender=Comment)
def create_comment_notification(sender, instance, created, **kwargs):
    """
    Create a comment type notification once the comment is created.
    """
    if created:
        sender_= instance.user
        receiver_ = instance.post.user
        if sender_ != receiver_:
            # create a comment type notification. 
            Notification.objects.create(sender=sender_, receiver=receiver_, notification_type='comment', 
                post=instance.post, comment=instance)