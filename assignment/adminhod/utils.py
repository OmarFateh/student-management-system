from django.db.models import Q

from assignment.models import Assignment, StudentAssignment
from adminhod.utils import filter_list

def search(q, assignment_qs=None):
    """
    Take search value, q.
    Take assignment queryset, filter the queryset by student's name and submission date, ordered alphabetically by student's name.
    """
    # filter assignments by student's name and submission date, ordered alphabetically by student's name.
    return assignment_qs.filter(
        Q(student__user__full_name__startswith=q)|
        Q(created_at__icontains=q)
    ).distinct().order_by('student__user__full_name')

def filter_adminhod_assignments(course_id=None, subject_id=None, session_year_id=None, subjects_ids_list=None):
    """
    Take course's id, subject's id, session's id values, and subjects ids list. 
    Filter assignments by Course, Subject, or Session Year.
    """
    # get list of submitted data.
    list_data = [course_id, subject_id, session_year_id]
    # give none value to all querysets as initial values.
    assignments_course_qs = None
    assignments_session_qs = None
    assignments_subject_qs = None
    if course_id:
        # filter assignments by selected course.
        assignments_course_qs = Assignment.objects.filter(subject__course__id=course_id)
        # if queryset doesn't exist.
        if not assignments_course_qs.exists():
            assignments_course_qs = 'Assignment Course'
    if session_year_id:
        # filter assignments by selected session.
        assignments_session_qs = Assignment.objects.filter(subject__id__in=subjects_ids_list, session_year__id=session_year_id)
        # if queryset doesn't exist.
        if not assignments_session_qs.exists():
            assignments_session_qs = 'Assignment Session'
    if subject_id:
        # filter assignments by selected subject.
        assignments_subject_qs = Assignment.objects.filter(subject__id=subject_id)
        # if queryset doesn't exist.
        if not assignments_subject_qs.exists():
            assignments_subject_qs = 'Assignment Subject'
    # make a list of all filter querysets. 
    filter_qs_list = [assignments_course_qs, assignments_session_qs, assignments_subject_qs]
    # if course, subject or session is selected.
    if any(list_data):
        # return the intersection between all querysets.
        return filter_list(filter_qs_list)     
    # if not.
    else:
        # return all assignments.
        return Assignment.objects.filter(subject__id__in=subjects_ids_list) 

def filter_adminhod_submitted_assignments(submitted=None, assignment=None):
    """
    Take submitted value and assignment.
    Filter submitted assignments of this assignment by submission date, whether before or after the deadline date. 
    """
    if submitted == "before":
        # get submitted assignments of this assignment, which submitted before deadline.
       return StudentAssignment.objects.filter(assignment=assignment, created_at__lt=assignment.deadline_date)
    elif submitted == "after":
        # get submitted assignments of this assignment, which submitted after deadline.
       return StudentAssignment.objects.filter(assignment=assignment, created_at__gt=assignment.deadline_date)
    else:
        # get all submitted assignments of this assignment.
       return StudentAssignment.objects.filter(assignment=assignment)