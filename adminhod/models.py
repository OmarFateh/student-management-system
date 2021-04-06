import os

from django.db import models
from django.conf import settings

from django_countries.fields import CountryField

from accounts.models import User

def adminhod_image(instance, filename):
    """
    Upload the adminhod image into the path and return the uploaded image path.
    """
    pic_extention = filename.split('.')[-1]
    profile_pic_name = f'adminhod/{instance.user.full_name}/profile.{pic_extention}'
    full_path = os.path.join(settings.MEDIA_ROOT, profile_pic_name)
    if os.path.exists(full_path):
        os.remove(full_path)
    return profile_pic_name

class UserCommonInfo(models.Model):
    """
    User common info model.
    """
    GENDER_CHOICES = (
        ('male', 'male'),
        ('female', 'female')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slug = models.CharField(max_length=10, unique=True, null=True, blank=True)
    birth_date = models.DateField(null=True)
    education = models.CharField(max_length=256, null=True, blank=True)
    skills = models.CharField(max_length=256, null=True, blank=True)
    nationality = CountryField()
    phone = models.CharField(max_length=17, null=True)
    address = models.CharField(max_length=256, null=True)
    gender = models.CharField(max_length=8, choices=GENDER_CHOICES, null=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        abstract = True

class AdminHOD(UserCommonInfo):
    """
    Adminhod model.
    """
    photo = models.ImageField(upload_to=adminhod_image, default='user_default.jpg')
    recruitment_date = models.DateField(null=True)

    class Meta:
        verbose_name = 'AdminHOD'
        verbose_name_plural = 'AdminHODs'
        ordering = ['user__full_name']

    def __str__ (self):
        # Return user name.
        return self.user.full_name    