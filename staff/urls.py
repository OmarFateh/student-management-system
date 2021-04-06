from django.urls import path

from .views import staff_dashboard, staff_profile    

urlpatterns = [
    # dashboard
    path('dashboard/staff/', staff_dashboard, name='dashboard'),
    # staff profile
    path('staff/profiles/<str:staff_slug>/', staff_profile, name='staff-profile'),
] 