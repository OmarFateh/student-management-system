from django.urls import path

from .views import (
    add_feedback_staff, 
    view_feedback_staff, 
    feedback_detail_staff, 
    filter_feedback_staff,
    paginate_feedback_staff,
)    

# namespace = 'feedback-staff'

urlpatterns = [
    # staff feedback
    path('feedback/staff/add/', add_feedback_staff, name='add-feedback'),
    path('feedback/staff/', view_feedback_staff, name='view-feedback'),
    path('feedback/staff/<int:feedback_id>/', feedback_detail_staff, name='feedback-detail'),
    path('ajax/feedback/staff/filter/', filter_feedback_staff, name='ajax-filter-staff-feedback'),
    path('ajax/feedback/staff/paginate/', paginate_feedback_staff, name='ajax-paginate-staff-feedback'),
] 