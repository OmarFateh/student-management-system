from django.urls import path

from .views import (
    add_staff, 
    manage_staff,
    paginate_staff,
    filter_staff,
    update_staff,
    delete_staff,
)    

# namespace = adminhod

urlpatterns = [
    # staff
    path('staff/add/', add_staff, name='add-staff'),
    path('staff/', manage_staff, name='manage-staff'),
    path('ajax/staff/paginate/', paginate_staff, name='ajax-paginate-staff'),
    path('ajax/staff/filter/', filter_staff, name='ajax-filter-staff'),
    path('staff/<int:staff_id>/update/', update_staff, name='update-staff'),
    path('staff/<int:staff_id>/delete/', delete_staff, name='delete-staff'),
]    