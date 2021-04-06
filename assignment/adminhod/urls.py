from django.urls import path

from .views import (
    view_assignments, 
    assignment_detail,  
    paginate_assignments,
    filter_assignments,
    view_submitted_assignments,
    paginate_submitted_assignments,
    filter_submitted_assignments,
)

# namespace = 'assignment-adminhod'

urlpatterns = [
    # assignments
    path('assignments/view/', view_assignments, name='view-assignments'),
    path('assignments/<int:assignment_id>/view/', assignment_detail, name='assignment-detail'),
    path('ajax/assignments/paginate/', paginate_assignments, name='ajax-paginate-assignments'),
    path('ajax/assignments/filter/', filter_assignments, name='ajax-filter-assignments'),
    path('assignments/submitted/<str:assignment_slug>/view/', view_submitted_assignments, name='view-submitted-assignments'),
    path('ajax/assignments/paginate/<str:assignment_slug>/submitted/', paginate_submitted_assignments, name='ajax-paginate-submitted-assignments'),
    path('ajax/assignments/filter/<str:assignment_slug>/submitted/', filter_submitted_assignments, name='ajax-filter-submitted-assignments'),    
]