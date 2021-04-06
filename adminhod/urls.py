from django.urls import path, include

from .views import admin_dashboard, update_adminhod_view 

# namespace = adminhod

urlpatterns = [
    # dashboard
    path('', admin_dashboard, name='dashboard'),
    # update student profile
    path('profile/update/', update_adminhod_view, name='update-adminhod-profile'),

    path('', include('adminhod.staff.urls')),
    path('', include('adminhod.student.urls')),
    path('', include('adminhod.session.urls')),
]    