from django.contrib import admin

from .models import Student, SessionYear

# models admin site registeration. 
admin.site.register(Student)
admin.site.register(SessionYear)