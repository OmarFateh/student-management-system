from django.urls import path

from .views import (
    view_feedback_staff_adminhod, 
    view_feedback_student_adminhod,
    paginate_staff_feedbacks,
    paginate_student_feedbacks,
    filter_student_feedbacks,
    filter_staff_feedbacks,
    reply_feedback_staff,
    reply_feedback_student,
)    

# namespace = 'feedback-adminhod'

urlpatterns = [
    # adminhod staff feedback
    path('feedback/staff/view/', view_feedback_staff_adminhod, name='view-staff-feedback'),
    path('feedback/staff/<int:feedback_id>/view', reply_feedback_staff, name='staff-feedback-detail'),
    path('ajax/feedback/adminhod/staff/paginate/', paginate_staff_feedbacks, name='ajax-paginate-staff-feedback'),
    path('ajax/feedback/adminhod/staff/filter/', filter_staff_feedbacks, name='ajax-filter-staff-feedback'),

    # adminhod student feedback
    path('feedback/student/view/', view_feedback_student_adminhod, name='view-student-feedback'),
    path('feedback/student/<int:feedback_id>/view', reply_feedback_student, name='student-feedback-detail'),
    path('ajax/feedback/adminhod/student/paginate/', paginate_student_feedbacks, name='ajax-paginate-student-feedback'),
    path('ajax/feedback/adminhod/student/filter/', filter_student_feedbacks, name='ajax-filter-student-feedback'),
] 