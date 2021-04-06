from django.urls import path

from .views import (
    add_results, 
    get_students_results,
    get_students_initial_results, 
    save_results,
)    

# namespace = 'result-staff'

urlpatterns = [
    # add results
    path('results/add/', add_results, name='add-results'),
    path('ajax/students/results/fetch/', get_students_results, name='ajax-fetch-students-results'),
    path('ajax/students/results/initial/fetch/', get_students_initial_results, name='ajax-fetch-students-initial-results'),
    path('ajax/results/save/', save_results, name='ajax-save-results'),
] 