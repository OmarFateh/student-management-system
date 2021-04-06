from django.urls import path

from .views import (
    # course
    add_course, 
    manage_course,
    paginate_course,
    update_course,
    delete_course,
    # subject 
    add_subject, 
    manage_subject,
    paginate_subject,
    filter_subject,
    update_subject,
    delete_subject,
)     

# namespace = course 

urlpatterns = [
    # course
    path('courses/add/', add_course, name='add-course'),
    path('courses/', manage_course, name='manage-course'),
    path('ajax/courses/paginate/', paginate_course, name='ajax-paginate-courses'),
    path('courses/<int:course_id>/update/', update_course, name='update-course'),
    path('courses/<int:course_id>/delete/', delete_course, name='delete-course'),
    # subject
    path('subjects/add/', add_subject, name='add-subject'),
    path('subjects/', manage_subject, name='manage-subject'),
    path('ajax/subjects/paginate/', paginate_subject, name='ajax-paginate-subjects'),
    path('ajax/subjects/filter/', filter_subject, name='ajax-filter-subjects'),
    path('subjects/<int:subject_id>/update/', update_subject, name='update-subject'),
    path('subjects/<int:subject_id>/delete/', delete_subject, name='delete-subject'),
]    