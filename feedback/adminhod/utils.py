from django.db.models import Q

from feedback.models import FeedbackStaff, FeedbackStudent
from adminhod.utils import filter_list

def search(q, staff_feedbacks_qs=None, student_feedbacks_qs=None, staffs_ids_list=None, courses_ids_list=None):
    """
    Take search value, q.
    In case of taking staff feedbacks queryset and staffs' ids list, filter the queryset by staff's name.
    In case of taking student feedbacks queryset and courses_ids_list, filter the queryset by students' names.
    """
    if staff_feedbacks_qs:
        # filter staffs' feedbacks by staffs' names, ordered alphabetically by staff's name.
        return staff_feedbacks_qs.filter(
            staff__user__id__in=staffs_ids_list, 
            staff__user__full_name__startswith=q
        ).order_by('staff__user__full_name')
    elif student_feedbacks_qs:
        # filter students' feedbacks by students' names, ordered alphabetically by student's name.
        return student_feedbacks_qs.filter(
            student__course__in=courses_ids_list,
            student__user__full_name__startswith=q
        ).order_by('student__user__full_name')

def filter_adminhod_staffs_feedbacks(is_replied=None, staffs_ids_list=None):
    """
    Take is replied value and staffs ids list. 
    Filter staffs' feedbacks by Reply.
    """
    # get all replied staffs' feedbacks of current adminhod's courses.
    if is_replied == '1':    
        return FeedbackStaff.objects.filter(staff__user__id__in=staffs_ids_list, is_replied=True)
    # get all unreplied staffs' feedbacks of current adminhod's courses.
    elif is_replied == '0': 
        return FeedbackStaff.objects.filter(staff__user__id__in=staffs_ids_list, is_replied=False)
    else:
        # get all staffs' feedbacks of current adminhod's courses.
        return FeedbackStaff.objects.filter(staff__user__id__in=staffs_ids_list)

def filter_adminhod_students_feedbacks(is_replied=None, course_id=None, session_year_id=None, courses_ids_list=None):
    """
    Take is replied, course's id, session's id values, and courses ids list. 
    Filter students' feedbacks by Course, Session or Reply.
    """
    # get list of submitted data.
    list_data = [course_id, session_year_id, is_replied]
    # give none value to all querysets as initial values.
    student_feedback_course_qs = None
    student_feedback_session_qs = None
    student_feedback_is_replied = None
    if course_id:
        # filter students' feedbacks by selected course.
        student_feedback_course_qs = FeedbackStudent.objects.filter(student__course__id=course_id)
        # if queryset doesn't exist.
        if not student_feedback_course_qs.exists():
            student_feedback_course_qs = 'Student Feedback Course'
    if session_year_id:
        # filter students' feedbacks by selected session.
        student_feedback_session_qs = FeedbackStudent.objects.filter(student__course__id__in=courses_ids_list, student__session_year__id=session_year_id)
        # if queryset doesn't exist.
        if not student_feedback_session_qs.exists():
            student_feedback_session_qs = 'Student Feedback Session'
    if is_replied:
        # get all replied students' feedbacks.
        if is_replied == '1':    
            student_feedback_is_replied = FeedbackStudent.objects.filter(student__course__id__in=courses_ids_list, is_replied=True)
        # get all unreplied students' feedbacks.
        elif is_replied == '0': 
            student_feedback_is_replied = FeedbackStudent.objects.filter(student__course__id__in=courses_ids_list, is_replied=False)
        # if queryset doesn't exist.
        if not student_feedback_is_replied.exists():
            student_feedback_is_replied = 'Student Feedback replied'        
    # make a list of all filter querysets.
    filter_qs_list = [student_feedback_course_qs, student_feedback_session_qs, student_feedback_is_replied]
    # if course, session or is_replied is selected.
    if any(list_data):
        # return the intersection between all querysets.
        return filter_list(filter_qs_list)     
    # if not.
    else:
        # get all students' feedbacks of current adminhod's courses.
        return FeedbackStudent.objects.filter(student__course__id__in=courses_ids_list)