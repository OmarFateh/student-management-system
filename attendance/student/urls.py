from django.urls import path

from .views import view_attendance, get_attendance_data

urlpatterns = [
    # view attendance
    path('attendance/view/', view_attendance, name='view-attendance'),
    path('ajax/attendance/data/fetch/', get_attendance_data, name='ajax-fetch-attendance-data'),
    
] 