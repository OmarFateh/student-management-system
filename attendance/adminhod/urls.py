from django.urls import path

from .views import view_attendance_adminhod, get_attendance_subjects, get_attendance_data_adminhod

# namespace = 'attendance-adminhod'

urlpatterns = [
    # view student attendance
    path('attendance/student/view/', view_attendance_adminhod, name='view-student-attendance'),
    path('ajax/attendance/student/data/fetch/', get_attendance_data_adminhod, name='ajax-fetch-student-attendance-data'),
    path('ajax/load/subjects/', get_attendance_subjects, name='ajax-fetch-subjects'),
] 