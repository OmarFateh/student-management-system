from feedback.models import FeedbackStaff, FeedbackStudent 
from course.models import Subject

def feedback_count(request):
    """
    Custom context processor for feedback count.
    """
    count_staff_feedback = 0
    count_student_feedback = 0
    total_feedback_count = 0
    # check if current user is authenticated or not.
    if request.user.is_authenticated and request.user.user_type == 'HOD':
        # get list of all staffs' ids of current adminhod's courses.
        staffs_ids_list = Subject.objects.staff_ids(request.user)
        # get all staffs' feedbacks of current adminhod courses.
        feedbacks = FeedbackStaff.objects.filter(staff__user__id__in=staffs_ids_list)
        # get feedback count.
        count_staff_feedback = FeedbackStaff.objects.feedback_staff_count(feedbacks, request.user)
        count_student_feedback = FeedbackStudent.objects.feedback_student_count(request.user)
        total_feedback_count = count_staff_feedback + count_student_feedback
    return {
        'count_staff_feedback':count_staff_feedback, 
        'count_student_feedback':count_student_feedback,
        'total_feedback_count':total_feedback_count,
        }  