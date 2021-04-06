from django.db.models import Q

from course.models import Subject
from adminhod.utils import filter_list

def search(q, course_subject_qs=None):
    """
    Take search value, q.
    Take a course or subject queryset, filter the queryset by name or code, ordered alphabetically by name.
    """
    # filter courses or subjects by name or code, ordered alphabetically by courses' or subject's name.
    return course_subject_qs.filter(
        Q(name__startswith=q)|
        Q(code__icontains=q)
    ).distinct().order_by('name')

def filter_subjects(course_id=None, staff_id=None, request=None):
    """
    Take course's id and staff's id values, and request. 
    Filter subjects by Course or Staff.
    """
    # get list of submitted data.
    list_data = [course_id, staff_id]
    # give none value to all querysets as initial values.
    subjects_course_qs = None
    subjects_staff_qs = None
    if course_id:
        # filter subjects by selected course.
        subjects_course_qs = Subject.objects.filter(course__id=course_id)
        # if queryset doesn't exist.
        if not subjects_course_qs.exists():
            subjects_course_qs = 'Subject Course'
    if staff_id:    
        # filter subjects by selected staff.
        subjects_staff_qs = Subject.objects.filter(staff__id=staff_id)
        # if queryset doesn't exist.
        if not subjects_staff_qs.exists():
            subjects_staff_qs = 'Subject Staff'
    # make a list of all filter querysets.
    filter_qs_list = [subjects_course_qs, subjects_staff_qs]
    # if course, session or gender is selected.
    if any(list_data):
        # return the intersection between all querysets.
        return filter_list(filter_qs_list)     
    # if not.
    else:
       # get all staffs of current adminhod's courses.
        return Subject.objects.user_subjects(request.user)