from django.urls import path

from .views import (
    view_assignments, 
    assignment_detail, 
    upload_assignment, 
    filter_student_assignments,
    paginate_student_assignments
)

# namespace = 'assignment-student'

urlpatterns = [
    # assignments
    path('assignments/student/view/', view_assignments, name='view-assignments'),
    path('assignments/student/<int:assignment_id>/', assignment_detail, name='assignment-detail'),
    path('assignments/student/<int:assignment_id>/upload/', upload_assignment, name='upload-assignment'),
    path('ajax/assignments/student/filter/', filter_student_assignments, name='ajax-filter-assignments'),
    path('ajax/assignments/student/paginate/', paginate_student_assignments, name='ajax-paginate-assignments'),
] 