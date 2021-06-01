from django.db import models
from django.conf import settings
from django.urls import reverse

from adminhod.models import UserCommonInfo


def student_image(instance, filename):
    """
    Upload the student image into the path and return the uploaded image path.
    """
    return f'student/{instance.user.full_name}/{filename}'


class SessionYear(models.Model):
    """
    Session Year model.
    """
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    date_range = models.CharField(max_length=24, null=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        verbose_name = 'Session'
        verbose_name_plural = 'Sessions'
        ordering = ['start_date']

    def __str__ (self):
        # Return session start and end date.
        return f'{self.start_date} To {self.end_date}'         

    def get_update_absolute_url(self):
        # Return absolute url of update session by its id.
        return reverse('adminhod:update-session', kwargs={'session_id': self.pk})

    def get_delete_absolute_url(self):
        # Return absolute url of delete session by its id.
        return reverse('adminhod:delete-session', kwargs={'session_id': self.pk})

     
class StudentManager(models.Manager):
    """
    Override the student model manager.
    """
    def get_students_list_data(self, subject, session_year_id, is_results=None):
        """
        Take subject and session year's id.
        Get list of students' results data in case of taking is_results value, 
        and if not, get list of all students' id and name. 
        """
        # get all students of a certain course and session year, ordered alphabetically by student's name.
        students = self.get_queryset().filter(course=subject.course, session_year__id=session_year_id).order_by('user__full_name')
        students_list_data= []
        if students.exists():
            for student in students:
                # add students' results data to list.
                if is_results and student.results.filter(subject=subject, student=student).exists():
                    student_data = {
                        'id':student.id, 
                        'name':student.user.full_name,
                        'assignment_one_marks':student.results.filter(subject=subject, student=student)[0].assignment_one_marks,
                        'assignment_two_marks':student.results.filter(subject=subject, student=student)[0].assignment_two_marks,
                        'assignment_three_marks':student.results.filter(subject=subject, student=student)[0].assignment_three_marks,
                        'assignment_four_marks':student.results.filter(subject=subject, student=student)[0].assignment_four_marks,
                        'assignment_five_marks':student.results.filter(subject=subject, student=student)[0].assignment_five_marks,
                        'final_exam_marks':student.results.filter(subject=subject, student=student)[0].final_exam_marks,
                    }
                # add students' id and name to list.    
                else:
                    student_data = {'id':student.id, 'name':student.user.full_name}    
                students_list_data.append(student_data)        
        return students_list_data            


class Student(UserCommonInfo):
    """
    Student model.
    """
    course = models.ForeignKey('course.Course', on_delete=models.CASCADE, null=True)
    photo = models.ImageField(upload_to=student_image, default='user_default.jpg')
    session_year = models.ForeignKey(SessionYear, on_delete=models.CASCADE, null=True)
    
    objects = StudentManager()

    class Meta:
        ordering = ['user__full_name']

    def __str__ (self):
        # Return user name.
        return self.user.full_name         

    def get_absolute_url(self):
        # Return absolute url of student profile by its slug.
        return reverse('student:student-profile', kwargs={'student_slug': self.slug})

    def get_update_absolute_url(self):
        # Return absolute url of update student by its id.
        return reverse('adminhod:update-student', kwargs={'student_id': self.pk})

    def get_delete_absolute_url(self):
        # Return absolute url of delete student by its id.
        return reverse('adminhod:delete-student', kwargs={'student_id': self.pk}) 

    def filename(self):
        # return file name of student's photo.
        return self.photo.name.split('/')[-1]