from django.db import models
from django.urls import reverse

def student_assignment(instance, filename):
    """
    Upload the student assignment into the path and return the uploaded assignment path.
    """
    full_path = f'student/{instance.student.user.full_name}/assignments/{filename}'
    return full_path

class AssignmentManager(models.Manager):
    """
    Assignment model manager.
    """
    def assignments_updated(self, student=None):
        """
        Take student in case of updating assignments for students.
        Update assignments after seeing them.
        """
        if student:
            # update assignments after seeing them for students.
            anncouncements_qs = self.get_queryset().filter(subject__in=student.course.subjects.all(), session_year__id=student.session_year.id).exclude(is_seen=student)
            for assignment in anncouncements_qs:
                assignment.is_seen.add(student)
        else:
            # update assignments after seeing them for adminhod.
            anncouncements_qs = self.get_queryset().filter(is_seen_admin=False).update(is_seen_admin=True)
        return anncouncements_qs

    def assignments_count(self, student=None):
        """
        Take student in case of counting all unseen assignments for students.
        Count all unseen assignments for each student or for adminhod.
        """
        if student:
            # count all unseen assignments for students.
            return self.get_queryset().filter(subject__in=student.course.subjects.all(), session_year__id=student.session_year.id).exclude(is_seen=student).count()
        else:
            # count all unseen assignments for adminhod.
            return self.get_queryset().exclude(is_seen_admin=True).count()

    def student_assignments(self, subjects_ids, user):
        """
        Take student and list of subject's ids of this student.
        Get all assignments of this student.
        """
        return self.get_queryset().filter(subject__id__in=subjects_ids, session_year__id=user.student.session_year.id)  

class Assignment(models.Model):
    """
    Assignment model.
    Assignment is created by staff. 
    """
    subject = models.ForeignKey("course.Subject", on_delete=models.CASCADE)
    session_year = models.ForeignKey('student.SessionYear', on_delete=models.CASCADE)
    content = models.TextField()
    deadline_date = models.DateField()
    slug = models.CharField(max_length=10, unique=True, null=True, blank=True)
    is_seen = models.ManyToManyField('student.Student', related_name='seen_assignments', blank=True)
    is_submitted = models.ManyToManyField('student.Student', related_name='submitted_assignments', blank=True)
    allow_submission_after_deadline = models.BooleanField(default=False, null=True)
    is_seen_admin = models.BooleanField(default=False, null=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)

    objects = AssignmentManager()
    
    class Meta:
        verbose_name = 'Assignment'
        verbose_name_plural = 'Assignments'
        ordering = ['-created_at']

    def __str__ (self):
        # Return assignment .
        return f'{self.subject} | {self.session_year} | {self.deadline_date}'    

    def get_absolute_url(self):
        # Return absolute url of assignment by its id.
        return reverse('assignment-student:assignment-detail', kwargs={'assignment_id': self.pk})

    def get_upload_absolute_url(self):
        # Return absolute url of upload assignment by its id.
        return reverse('assignment-student:upload-assignment', kwargs={'assignment_id': self.pk})    

    def get_update_absolute_url(self):
        # Return absolute url of update assignment by its id.
        return reverse('assignment-staff:update-assignment', kwargs={'assignment_id': self.pk})

    def get_delete_absolute_url(self):
        # Return absolute url of delete assignment by its id.
        return reverse('assignment-staff:delete-assignment', kwargs={'assignment_id': self.pk})   

    def get_submitted_assignments_absolute_url(self):
        # Return absolute url of submitted assignments by its slug.
        return reverse('assignment-staff:view-submitted-assignments', kwargs={'assignment_slug': self.slug})

    def get_submitted_assignments_adminhod_absolute_url(self):
        # Return absolute url of submitted assignments for adminhod by its slug.
        return reverse('assignment-adminhod:view-submitted-assignments', kwargs={'assignment_slug': self.slug})              

class StudentAssignment(models.Model):
    """
    Student Assignment model.
    Assignment is uploaded by students.
    """
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, null=True,blank=True)
    student = models.ForeignKey('student.Student', on_delete=models.CASCADE, related_name='assignments', null=True, blank=True)
    document = models.FileField(upload_to=student_assignment, null=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        verbose_name = 'Student Assignment'
        verbose_name_plural = 'Student Assignments'
        ordering = ['-created_at']

    def __str__ (self):
        # Return assignment .
        return f'{self.assignment} | {self.student}'
