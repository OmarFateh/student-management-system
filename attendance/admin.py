from django.contrib import admin

from .models import Attendance, AttendanceReport

# models admin site registeration. 
admin.site.register(Attendance)
admin.site.register(AttendanceReport)