from django.urls import path

from .views import view_announcements_staff, add_announcement_staff, delete_announcement_staff

# namespace = 'announcement-staff'

urlpatterns = [
    # view announcements
    path('announcements/staff/view/', view_announcements_staff, name='view-announcements'),

    # add announcements
    path('announcements/staff/add/', add_announcement_staff, name='add-announcements'),

    # delete announcements
    path('announcements/staff/<int:announcement_id>/delete/', delete_announcement_staff, name='delete-announcements'),
] 