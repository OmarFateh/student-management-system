from django.urls import path

from .views import view_announcements_adminhod, add_announcement_adminhod, delete_announcement_adminhod

# namespace = 'announcement-adminhod'

urlpatterns = [
    # view announcements
    path('announcements/', view_announcements_adminhod, name='view-announcements'),

    # add announcements
    path('announcements/add/', add_announcement_adminhod, name='add-announcements'),

    # delete announcements
    path('announcements/<int:announcement_id>/delete/', delete_announcement_adminhod, name='delete-announcements'),
] 