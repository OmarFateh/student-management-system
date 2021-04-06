from django.urls import path

from .views import (
    add_feedback_student, 
    view_feedback_student, 
    feedback_detail_student, 
    filter_feedback_student,
    paginate_feedback_student,
)    

# namespace = 'feedback-student'

urlpatterns = [
    # student feedback
    path('feedback/student/add/', add_feedback_student, name='add-feedback'),
    path('feedback/student/', view_feedback_student, name='view-feedback'),
    path('feedback/student/<int:feedback_id>/', feedback_detail_student, name='feedback-detail'),
    path('ajax/feedback/student/filter/', filter_feedback_student, name='ajax-filter-student-feedback'),
    path('ajax/feedback/student/paginate/', paginate_feedback_student, name='ajax-paginate-student-feedback'),
] 