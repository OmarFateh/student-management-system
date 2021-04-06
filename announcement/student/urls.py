from django.urls import path

from .views import view_announcements_student

# namespace = 'announcement-student'

urlpatterns = [
    # view announcements
    path('announcements/student/view/', view_announcements_student, name='view-announcements'),

] 