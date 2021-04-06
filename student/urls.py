from django.urls import path

from .views import (
    student_dashboard, 
    student_profile,
)        

urlpatterns = [
    # dashboard
    path('dashboard/student/', student_dashboard, name='dashboard'),
    # student profile
    path('student/profiles/<str:student_slug>/', student_profile, name='student-profile'),
] 