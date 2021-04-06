from django.urls import path

from .views import view_results_adminhod, get_results_data_adminhod

# namespace = 'result-adminhod'

urlpatterns = [
    # view student results
    path('results/student/view/', view_results_adminhod, name='view-student-results'),
    path('ajax/results/student/data/fetch/', get_results_data_adminhod, name='ajax-fetch-student-results-data'),
] 