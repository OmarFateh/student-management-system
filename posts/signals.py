from django.dispatch import receiver
from django.db.models.signals import pre_save

from .models import Post
from adminhod.utils import unique_slug_generator

@receiver(pre_save, sender=Post)     # receiver(signal, **kwargs) # to register a signal
def create_post_slug(sender, instance, *args, **kwargs):
    """
    Create a slug for an post before saving.
    """
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)