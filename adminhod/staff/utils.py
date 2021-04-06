from course.models import Subject
from staff.models import Staff
from adminhod.utils import filter_list

def filter_staffs(course_id=None, gender=None, staffs_ids_list=None):
    """
    Take course's id value, gender and staffs ids list. 
    Filter staffs by Course or Gender.
    """
    # get list of submitted data.
    list_data = [course_id, gender]
    # give none value to all querysets as initial values.
    staffs_course_qs = None
    staffs_gender_qs = None
    if course_id:
        # get list of all staffs' ids of selected course.
        staff_ids_list = Subject.objects.course_staffs_ids(course_id)
        # get all staffs of selected course.
        staffs_course_qs = Staff.objects.filter(user__id__in=staff_ids_list)
        # if queryset doesn't exist.
        if not staffs_course_qs.exists():
            staffs_course_qs = 'Staff Course'
    if gender:
        # filter staffs by selected gender.
        staffs_gender_qs = Staff.objects.filter(user__id__in=staffs_ids_list, gender=gender)
        # if queryset doesn't exist.
        if not staffs_gender_qs.exists():
            staffs_gender_qs = 'Staff Gender'
    # make a list of all filter querysets.
    filter_qs_list = [staffs_course_qs, staffs_gender_qs]
    # if course, session or gender is selected.
    if any(list_data):
        # return the intersection between all querysets.
        return filter_list(filter_qs_list)     
    # if not.
    else:
       # get all staffs of current adminhod's courses.
        return Staff.objects.filter(user__id__in=staffs_ids_list) 