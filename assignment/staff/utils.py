from assignment.models import Assignment, StudentAssignment
from adminhod.utils import filter_list

def filter_staffs_assignments(course_id=None, subject_id=None, session_year_id=None, subjects_ids=None):
    """
    Take course's id, subject's id, session's id values, and subjects ids list. 
    Filter assignments by Course, Subject, or Session Year.
    """
    # get list of submitted data.
    list_data = [course_id, subject_id, session_year_id]
    # give none value to all querysets as initial values.
    assignments_course_qs = None
    assignments_subject_qs = None
    assignments_session_qs = None
    if course_id:
        # filter assignments by selected course.
        assignments_course_qs = Assignment.objects.filter(subject__course__id=course_id, subject__id__in=subjects_ids) 
        # if queryset doesn't exist.
        if not assignments_course_qs.exists():
            assignments_course_qs = 'Assignment Course'
    if subject_id:
        # filter assignments by selected subject.
        assignments_subject_qs = Assignment.objects.filter(subject__id=subject_id) 
        # if queryset doesn't exist.
        if not assignments_subject_qs.exists():
            assignments_subject_qs = 'Assignment Subject'
    if session_year_id:
        # filter assignments by selected session.
        assignments_session_qs = Assignment.objects.filter(subject__id__in=subjects_ids, session_year__id=session_year_id)
        # if queryset doesn't exist.
        if not assignments_session_qs.exists():
            assignments_session_qs = 'Assignment Session'        
    # make a list of all filter querysets.
    filter_qs_list = [assignments_course_qs, assignments_subject_qs, assignments_session_qs]
    # if course or subject is selected.
    if any(list_data):
        # return the intersection between all querysets.
        return filter_list(filter_qs_list)                
    # if not.
    else:
        # get all assignments of current staff.
        return Assignment.objects.filter(subject__id__in=subjects_ids)

def filter_staffs_submitted_assignments(submitted=None, assignment=None):
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