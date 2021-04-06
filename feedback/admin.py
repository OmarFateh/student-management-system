from django.contrib import admin

from .models import FeedbackStaff, FeedbackStudent

# models admin site registeration. 
admin.site.register(FeedbackStaff)
admin.site.register(FeedbackStudent)