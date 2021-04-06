from django.contrib import admin

from .models import Course, Subject

# models admin site registeration. 
admin.site.register(Course)
admin.site.register(Subject)
