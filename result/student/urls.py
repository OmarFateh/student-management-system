from django.urls import path

from .views import view_results, get_results_data

# namespace = 'result-student'

urlpatterns = [
    # view results
    path('results/view/', view_results, name='view-results'),
    path('ajax/results/data/fetch/', get_results_data, name='ajax-fetch-results-data'),
    
] 