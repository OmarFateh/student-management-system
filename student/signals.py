from django.dispatch import receiver
from django.db.models.signals import pre_save

from adminhod.utils import unique_slug_generator
from .models import Student

@receiver(pre_save, sender=Student)     # receiver(signal, **kwargs) # to register a signal
def create_student_slug(sender, instance, *args, **kwargs):
    """
    Create a unique slug for a student before saving.
    """
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)