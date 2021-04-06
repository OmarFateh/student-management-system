from student.models import Student
from adminhod.utils import filter_list

def filter_students(course_id=None, session_year_id=None, gender=None, courses_ids_list=None):
    """
    Take course's id and session's id values, gender and courses ids list. 
    Filter students by Course, Session or Gender.
    """
    # get list of submitted data.
    list_data = [course_id, session_year_id, gender]
    # give none value to all querysets as initial values.
    students_course_qs = None
    students_session_qs = None
    students_gender_qs = None
    if course_id:
        # filter students by selected course.
        students_course_qs = Student.objects.filter(course__id=course_id)
        # if queryset doesn't exist.
        if not students_course_qs.exists():
            students_course_qs = 'Student Course'
    if session_year_id:
        # filter students by selected session.
        students_session_qs = Student.objects.filter(course__id__in=courses_ids_list, session_year__id=session_year_id)
        # if queryset doesn't exist.
        if not students_session_qs.exists():
            students_session_qs = 'Student Session'
    if gender:
        # filter students by selected gender.
        students_gender_qs = Student.objects.filter(course__id__in=courses_ids_list, gender=gender)
        # if queryset doesn't exist.
        if not students_gender_qs.exists():
            students_gender_qs = 'Student Gender'
    # make a list of all filter querysets.
    filter_qs_list = [students_course_qs, students_session_qs, students_gender_qs]
    # if course, session or gender is selected.
    if any(list_data):
        # return the intersection between all querysets.
        return filter_list(filter_qs_list)     
    # if not.
    else:
        # get all students of current adminhod's courses.
        return Student.objects.filter(course__id__in=courses_ids_list)
