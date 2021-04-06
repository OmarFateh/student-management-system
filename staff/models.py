import os

from django.db import models
from django.conf import settings
from django.urls import reverse

from django_countries.fields import CountryField

from adminhod.models import UserCommonInfo

def staff_image(instance, filename):
    """
    Upload the staff image into the path and return the uploaded image path.
    """
    pic_extention = filename.split('.')[-1]
    profile_pic_name = f'staff/{instance.user.full_name}/profile.{pic_extention}'
    full_path = os.path.join(settings.MEDIA_ROOT, profile_pic_name)
    if os.path.exists(full_path):
        os.remove(full_path)
    return profile_pic_name


class Staff(UserCommonInfo):
    """
    Staff model.
    """
    photo = models.ImageField(upload_to=staff_image, default='user_default.jpg')
    recruitment_date = models.DateField(null=True)
    
    class Meta:
        verbose_name = 'Staff'
        verbose_name_plural = 'Staffs'
        ordering = ['user__full_name']
        
    def __str__ (self):
        # Return user name.
        return self.user.full_name

    def get_absolute_url(self):
        # Return absolute url of staff profile by its slug.
        return reverse('staff:staff-profile', kwargs={'staff_slug': self.slug})

    def get_update_absolute_url(self):
        # Return absolute url of update staff by its id.
        return reverse('adminhod:update-staff', kwargs={'staff_id': self.pk})

    def get_delete_absolute_url(self):
        # Return absolute url of delete staff by its id.
        return reverse('adminhod:delete-staff', kwargs={'staff_id': self.pk})    

    def filename(self):
        # return file name of staff's photo.
        return self.photo.name.split('/')[-1]    