from django.urls import path

from .views import staff_feed

# namespace = feed-staff 

urlpatterns = [
    path('staff/feed/', staff_feed, name='staff-feed'),
]