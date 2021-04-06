from feedback.models import FeedbackStaff

def filter_staffs_feedbacks(is_replied=None, request=None):
    """
    Take is replied value and request. 
    Filter current staff's feedbacks by Reply.
    """
    # get all replied staff's feedbacks.
    if is_replied == '1':    
        return FeedbackStaff.objects.filter(staff__user__id=request.user.id, is_replied=True)
    # get all unreplied staff's feedbacks.
    elif is_replied == '0': 
        return FeedbackStaff.objects.filter(staff__user__id=request.user.id, is_replied=False)
    else:
        # get all staff's feedbacks.
        return FeedbackStaff.objects.filter(staff__user__id=request.user.id) 