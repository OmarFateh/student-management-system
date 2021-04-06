from django.urls import path

from .views import (
    add_assignment, 
    manage_assignment,
    filter_assignments,
    get_subjects,
    paginate_assignments,
    update_assignment,
    delete_assignment,
    view_submitted_assignments,
    paginate_submitted_assignments,
    filter_submitted_assignments,
)

# namespace = 'assignment-staff'

urlpatterns = [
    # assignments
    path('assignments/staff/add/', add_assignment, name='add-assignment'),
    path('assignments/staff/view/', manage_assignment, name='manage-assignment'),
    path('ajax/load/staff/subjects/', get_subjects, name='ajax-fetch-subjects-staff'),
    path('ajax/assignments/staff/filter/', filter_assignments, name='ajax-filter-assignments'),
    path('ajax/assignments/staff/paginate/', paginate_assignments, name='ajax-paginate-assignments'),
    path('assignments/<int:assignment_id>/update/', update_assignment, name='update-assignment'),
    path('assignments/<int:assignment_id>/delete/', delete_assignment, name='delete-assignment'),
    path('assignments/staff/<str:assignment_slug>/view/', view_submitted_assignments, name='view-submitted-assignments'),
    path('ajax/assignments/staff/paginate/<str:assignment_slug>/submitted/', paginate_submitted_assignments, name='ajax-paginate-submitted-assignments'),
    path('ajax/assignments/staff/filter/<str:assignment_slug>/submitted/', filter_submitted_assignments, name='ajax-filter-submitted-assignments'),
] 