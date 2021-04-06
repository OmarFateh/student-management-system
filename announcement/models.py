from django.db import models
from django.urls import reverse
from django.db.models import Q

class AnnouncementManager(models.Manager):
    """
    Announcement model manager.
    """
    def announcements_updated(self, user, staffs_ids_list, adminhod_ids_list=None, is_student=None, is_staff=None):
        """
        Take user, and update announcements of this user after seeing them.
        """
        if is_student: 
            announcements_qs = self.get_queryset().filter(
                Q(adminhod=user.student.course.adminhod)|
                Q(staff__user__id__in=staffs_ids_list))
        elif is_staff:
            announcements_qs = self.get_queryset().filter(
                Q(adminhod__id__in=adminhod_ids_list)|
                Q(staff__user__id__in=staffs_ids_list))
        else:
            announcements_qs = self.get_queryset().filter(
                Q(adminhod=user.adminhod)|
                Q(staff__user__id__in=staffs_ids_list))
        for announcement in announcements_qs.distinct().exclude(is_seen=user):
            announcement.is_seen.add(user)
        return announcements_qs

    def announcements_count(self, user, staffs_ids_list, adminhod_ids_list=None, is_student=None, is_staff=None):
        """
        Take user, and count all unseen announcements of this user.
        """
        if is_student:
            announcements_qs = self.get_queryset().filter(
                Q(adminhod=user.student.course.adminhod)|
                Q(staff__user__id__in=staffs_ids_list))
        elif is_staff:
            announcements_qs = self.get_queryset().filter(
                Q(adminhod__id__in=adminhod_ids_list)|
                Q(staff__user__id__in=staffs_ids_list))
        else:
            announcements_qs = self.get_queryset().filter(
                Q(adminhod=user.adminhod)|
                Q(staff__user__id__in=staffs_ids_list))
        return announcements_qs.distinct().exclude(is_seen=user).count()

class Announcement(models.Model):
    """
    Announcement model.
    """
    adminhod = models.ForeignKey('adminhod.AdminHOD', on_delete=models.CASCADE, null=True, blank=True, related_name='announcements')
    staff = models.ForeignKey('staff.Staff', on_delete=models.CASCADE, null=True, blank=True, related_name='announcements')
    header = models.CharField(max_length=100, null=True, blank=True)
    content = models.TextField()
    is_adminhod = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_seen = models.ManyToManyField('accounts.User', related_name='seen_announcements', blank=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)

    objects = AnnouncementManager()

    class Meta:
        verbose_name = 'Announcement'
        verbose_name_plural = 'Announcements'
        ordering = ['-created_at']

    def __str__ (self):
        # Return staff or adminhod name.
        if self.is_adminhod:
            return self.adminhod.user.full_name
        elif self.is_staff:      
            return self.staff.user.full_name

    def get_delete_absolute_url(self):
        if self.adminhod:
            # Return absolute url of delete announcement-adminhod by its id.
            return reverse('announcement-adminhod:delete-announcements', kwargs={'announcement_id': self.pk})
        elif self.staff:
            # Return absolute url of delete announcement-staff by its id.
            return reverse('announcement-staff:delete-announcements', kwargs={'announcement_id': self.pk})