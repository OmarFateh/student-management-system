from django.db.models import Q

from feedback.models import FeedbackStudent

def filter_students_feedbacks(is_replied=None, request=None):
    """
    Take is replied value and request. 
    Filter current student's feedbacks by Reply.
    """
    # get all replied student's feedbacks.
    if is_replied == '1':    
        return FeedbackStudent.objects.filter(student__user__id=request.user.id, is_replied=True)
    # get all unreplied student's feedbacks.
    elif is_replied == '0': 
        return FeedbackStudent.objects.filter(student__user__id=request.user.id, is_replied=False)
    else:
        # get all student's feedbacks.
        return FeedbackStudent.objects.filter(student__user__id=request.user.id)