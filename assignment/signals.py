from django.dispatch import receiver
from django.db.models.signals import pre_save

from adminhod.utils import unique_slug_generator
from .models import Assignment

@receiver(pre_save, sender=Assignment)     # receiver(signal, **kwargs) # to register a signal
def create_assignment_slug(sender, instance, *args, **kwargs):
    """
    Create a unique slug for an assignment before saving.
    """
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)