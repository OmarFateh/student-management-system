from django.urls import path

from .views import (
    take_attendance, 
    get_students, 
    save_attendance,
    manage_attendance,
    get_attendance_dates,
    get_attendance_students,
    update_attendance,
)    

urlpatterns = [
    # take attendance
    path('attendance/take/', take_attendance, name='take-attendance'),
    path('ajax/students/fetch/', get_students, name='ajax-fetch-students'),
    path('ajax/attendance/save/', save_attendance, name='ajax-save-attendance'),
    # manage attendance
    path('attendance/', manage_attendance, name='manage-attendance'),
    path('ajax/attendance/dates/fetch/', get_attendance_dates, name='ajax-fetch-attendance-dates'),
    path('ajax/attendance/students/fetch/', get_attendance_students, name='ajax-fetch-attendance-students'),
    path('ajax/attendance/update/', update_attendance, name='ajax-update-attendance'),

]    