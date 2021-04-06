from django.contrib import admin

from .models import  Assignment, StudentAssignment

# models admin site registeration.
admin.site.register(Assignment) 
admin.site.register(StudentAssignment)
