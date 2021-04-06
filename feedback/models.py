from django.db import models
from django.urls import reverse

from staff.models import Staff 
from student.models import Student 

class FeedbackStaffManager(models.Manager):
    """
    Feedback staff model manager.
    """
    def feedback_staff_updated(self, staff_feedbacks_qs, user):
        """
        Take adminhod and his staff feedbacks, and update staff feedbacks after seeing them.
        """
        for staff_feedback in staff_feedbacks_qs:
            staff_feedback.is_seen.add(user.adminhod)
        return staff_feedbacks_qs

    def feedback_staff_count(self, staff_feedbacks_qs, user):
        """
        Take adminhod and his staff feedbacks, and count all staff feedbacks.
        """
        return staff_feedbacks_qs.exclude(is_seen=user.adminhod).count()

class FeedbackStaff(models.Model):
    """
    Feedback staff model.
    """
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    content = models.TextField()
    reply = models.TextField()
    is_replied = models.BooleanField(default=False)
    is_seen = models.ManyToManyField('adminhod.AdminHOD', related_name='seen_staff_feedbacks', blank=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)

    objects = FeedbackStaffManager()

    class Meta:
        verbose_name = 'Feedback Staff'
        verbose_name_plural = 'Feedback Staff'
        ordering = ['-created_at']

    def __str__ (self):
        # Return user name.
        return self.staff.user.full_name  

    def get_absolute_url(self):
        # Return absolute url of staff feedback by its id.
        return reverse('feedback-staff:feedback-detail', kwargs={'feedback_id': self.pk}) 

    def get_absolute_url_adminhod(self):
        # Return absolute url of staff feedback for adminhod by its id.
        return reverse('feedback-adminhod:staff-feedback-detail', kwargs={'feedback_id': self.pk})            

class FeedbackStudentManager(models.Manager):
    """
    Feedback student model manager.
    """
    def feedback_student_updated(self, user):
        """
        Take adminhod, and update student feedbacks of this adminhod after seeing them.
        """
        student_feedbacks_qs = self.get_queryset().filter(
            student__course__in=user.adminhod.courses.all()).exclude(is_seen=user.adminhod)
        for student_feedback in student_feedbacks_qs:
            student_feedback.is_seen.add(user.adminhod)
        return student_feedbacks_qs
        
    def feedback_student_count(self, user):
        """
        Take adminhod, and count all student feedbacks of this adminhod.
        """
        return self.get_queryset().filter(
            student__course__in=user.adminhod.courses.all()).exclude(is_seen=user.adminhod).count()
        
class FeedbackStudent(models.Model):
    """
    Feedback student model.
    """
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    content = models.TextField()
    reply = models.TextField()
    is_replied = models.BooleanField(default=False)
    is_seen = models.ManyToManyField('adminhod.AdminHOD', related_name='seen_student_feedbacks', blank=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)

    objects = FeedbackStudentManager()

    class Meta:
        verbose_name = 'Feedback Student'
        verbose_name_plural = 'Feedback Student'
        ordering = ['-created_at']

    def __str__ (self):
        # Return user name.
        return self.student.user.full_name

    def get_absolute_url(self):
        # Return absolute url of student feedback by its id.
        return reverse('feedback-student:feedback-detail', kwargs={'feedback_id': self.pk})        

    def get_absolute_url_adminhod(self):
        # Return absolute url of student feedback for adminhod by its id.
        return reverse('feedback-adminhod:student-feedback-detail', kwargs={'feedback_id': self.pk})    