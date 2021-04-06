from django.urls import path

from .views import (
    add_student, 
    manage_student,
    paginate_student,
    filter_student,
    update_student,
    delete_student,
    
)    

# namespace = adminhod

urlpatterns = [
    # student
    path('students/add/', add_student, name='add-student'),
    path('students/', manage_student, name='manage-student'),
    path('ajax/students/paginate/', paginate_student, name='ajax-paginate-students'),
    path('ajax/students/filter/', filter_student, name='ajax-filter-students'),
    path('students/<int:student_id>/update/', update_student, name='update-student'),
    path('students/<int:student_id>/delete/', delete_student, name='delete-student'),
] 