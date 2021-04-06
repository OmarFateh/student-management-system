from course.models import Subject
from assignment.models import Assignment
from adminhod.utils import filter_list

def filter_students_assignments(subject_id=None, is_submitted=None, request=None):
    """
    Take subject's id, is sumbitted values, and request. 
    Filter assignments of current student by Subject or whether it's been submitted or not.
    """
    # get list of submitted data.
    list_data = [subject_id, is_submitted]
    # give none value to all querysets as initial values.
    assignments_subject_qs = None
    assignments_is_submitted = None
    if subject_id:
        # filter assignments by selected subject.
        assignments_subject_qs = Assignment.objects.filter(subject__id=subject_id, session_year__id=request.user.student.session_year.id)
        # if queryset doesn't exist.
        if not assignments_subject_qs.exists():
            assignments_subject_qs = 'Assignment subject'
    if is_submitted:
        # get all submitted assignments.
        if is_submitted == '1':    
            assignments_is_submitted = Assignment.objects.filter(is_submitted=request.user.student, session_year__id=request.user.student.session_year.id)
        # get all unsubmitted assignments.
        elif is_submitted == '0': 
            assignments_is_submitted = Assignment.objects.filter(session_year__id=request.user.student.session_year.id).exclude(is_submitted=request.user.student)
        # if queryset doesn't exist.
        if not assignments_is_submitted.exists():
            assignments_is_submitted = 'Assignment submitted'       
    # make a list of all filter querysets.
    filter_qs_list = [assignments_subject_qs, assignments_is_submitted]
    # if subject or submission is selected.
    if any(list_data):
        # return the intersection between all querysets.
        return filter_list(filter_qs_list)       
    # if not.
    else:
        # get all subjects ids of current student.
        subjects_ids = Subject.objects.student_subjects_ids(request.user)
        # get all assignments of current student.
        return Assignment.objects.student_assignments(subjects_ids, request.user)