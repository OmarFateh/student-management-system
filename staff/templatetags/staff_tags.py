from django import template

from course.models import Subject

register = template.Library()

@register.simple_tag
def staff_subjects(staff, user=None):
    """
    Take Staff only, and get all subjects of this staff.
    Take staff and user, and get all subjects of this staff, which are in this user's course.
    """
    if user:
        # if the user is a student.
        try:
            subjects = Subject.objects.filter(course=user.student.course, staff=staff)
        # if the user is a staff.
        except:
            # get list of all courses' ids of current staff.
            courses_ids_list = Subject.objects.courses_ids(user)
            # get all subjects of selsected staff which are in the same courses as the current staff.
            subjects = Subject.objects.filter(course__id__in=courses_ids_list, staff=staff)
    else:
        subjects = Subject.objects.filter(staff=staff)
    subjects_list = [subject.name for subject in subjects]    
    return subjects_list