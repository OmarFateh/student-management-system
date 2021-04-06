from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import User
from student.models import Student
from staff.models import Staff
from adminhod.models import AdminHOD


@receiver(post_save, sender=User)     
def create_user_profile(sender, instance, created, **kwargs):
    """
    Create an empty profile for each user type once the user is added.
    """
    if created:
        if instance.user_type == 'HOD':
            AdminHOD.objects.create(user=instance)
        elif instance.user_type == 'STAFF':   
            Staff.objects.create(user=instance)
        elif instance.user_type == 'STUDENT':    
            Student.objects.create(user=instance) 