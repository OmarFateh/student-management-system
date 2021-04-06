from django.db import models
from django.urls import reverse

class Course(models.Model):
    """
    Course model.
    """
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=64, unique=True)
    adminhod = models.ForeignKey('adminhod.AdminHOD', on_delete=models.SET_NULL, null=True, related_name='courses')
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'
        ordering = ['start_date']

    def __str__ (self):
        # Return course name.
        return self.name

    def get_update_absolute_url(self):
        # Return absolute url of update course by its id.
        return reverse('course:update-course', kwargs={'course_id': self.pk})

    def get_delete_absolute_url(self):
        # Return absolute url of delete course by its id.
        return reverse('course:delete-course', kwargs={'course_id': self.pk})         

class SubjectManager(models.Manager):
    """
    Subject model manager. 
    """
    def get_subjects_list_data(self, course_id=None, is_staff_assignment=None, user=None):
        """
        Get list of subjects' id and name of a certain course in case of taking course's id,
        Get list of subjects' id and name of a certain course and staff in case of taking course's id, 
        is_staff_assignment, and user, 
        and if not, get list of all subjects' id and name. 
        """
        subjects_list_data= []
        if course_id and is_staff_assignment:
            # get all subjects of current staff and of this course, ordered by name.
            subjects = self.get_queryset().filter(course__id=course_id, staff__user__id=user.id).order_by('name')
        elif course_id:
            # get all subjects of this course, ordered by name.
            subjects = self.get_queryset().filter(course__id=course_id).order_by('name')
        else:
            # get all subjects.
            subjects = self.get_queryset().all()
        if subjects.exists():
            for subject in subjects:
                subject_data = {'id':subject.id, 'name':subject.name}
                subjects_list_data.append(subject_data)
        return subjects_list_data
    
    def student_subjects_ids(self, user):
        """
        Take student, and get list of all subjects ids of this student.
        """
        return self.get_queryset().filter(course__student__user__id=user.id).values_list('id', flat=True)
    
    def user_subjects(self, user, is_ids=None, is_student=None, is_staff=None):
        """
        Take user, and get list of all subjects or their ids of this user's courses.
        """
        if is_student:
            # get all subjects of current student's course.
            subjects = self.get_queryset().filter(course__id=user.student.course.id)
        elif is_staff:
            # get all subjects of current staff's courses.
            subjects = self.get_queryset().filter(course__id__in=self.courses_ids(user))
        else:
            # get list of all courses' ids of current adminhod.
            courses_ids_list = Course.objects.filter(adminhod__user__id=user.id).values_list('id', flat=True)
            # get all subjects of current adminhod's courses.
            subjects = self.get_queryset().filter(course__id__in=courses_ids_list)
        # get list of all subjects' ids of current user's courses.
        subjects_ids_list = subjects.values_list('id', flat=True)
        if is_ids:
            return subjects_ids_list
        else:
            return subjects  

    def staff_ids(self, user, is_student=None, is_staff=None):
        """
        Take user, and get list of all staffs or their ids of this user's courses.
        """
        if is_student:
            # get list of all staffs' ids of current student's course.
            staffs_ids_list = [subject.staff.user.id for subject in self.user_subjects(user, is_student=True)]
        elif is_staff:
            # get list of all staffs' ids of current staff's courses.
            staffs_ids_list = [subject.staff.user.id for subject in self.user_subjects(user, is_staff=True)]
        else:    
            # get list of all staffs' ids of current adminhod's courses.
            staffs_ids_list = [subject.staff.user.id for subject in self.user_subjects(user)]
        return staffs_ids_list 
    
    def courses_adminhods_ids(self, user):
        """
        Take user, and get list of all adminhods' ids of this user's courses.
        """
        # get all subjects of current staff.
        staff_subjects = self.get_queryset().filter(staff__user__id=user.id)
        # get list of all adminhods' ids of current staff's courses.
        courses_adminhod_ids_list = [subject.course.adminhod.id for subject in staff_subjects]
        return courses_adminhod_ids_list

    def courses_ids(self, user):
        """
        Take user, and get list of all courses or their ids of this user.
        """
        # get all subjects of current staff.
        staff_subjects = self.get_queryset().filter(staff__id=user.staff.id)
        # get list of all courses' ids of current staff.
        courses_ids_list = [subject.course.id for subject in staff_subjects]
        return courses_ids_list

    def course_staffs_ids(self, course_id):
        """
        Take course id, and get list of all staffs' ids of this course.
        """
        # get all subjects of given course.
        subjects_course_qs = self.get_queryset().filter(course__id=course_id) 
        # get list of all staffs' ids of this course.
        staffs_ids_list = [subject.staff.user.id for subject in subjects_course_qs] 
        return staffs_ids_list

        
class Subject(models.Model):
    """
    Subject model.
    """
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=64, unique=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='subjects')
    staff = models.ForeignKey('staff.Staff', on_delete=models.SET_NULL, null=True, related_name='subjects')
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)

    objects = SubjectManager()

    class Meta:
        verbose_name = 'Subject'
        verbose_name_plural = 'Subjects'
        ordering = ['start_date']

    def __str__ (self):
        # Return subject name.
        return f"{self.name} | {self.course.name}"    

    def get_update_absolute_url(self):
        # Return absolute url of update subject by its id.
        return reverse('course:update-subject', kwargs={'subject_id': self.pk})

    def get_delete_absolute_url(self):
        # Return absolute url of delete subject by its id.
        return reverse('course:delete-subject', kwargs={'subject_id': self.pk})         