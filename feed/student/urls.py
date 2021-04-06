from django.urls import path

from .views import student_feed

# namespace = feed-student 

urlpatterns = [
    path('student/feed/', student_feed, name='student-feed'),
]