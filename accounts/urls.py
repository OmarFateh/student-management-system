from django.urls import path

from .views import (
    user_login_view, 
    user_logout_view, 
    change_password, 
    change_password_done,
    validate_email_view,
    validate_email_update_view
)

# namespace = accounts

urlpatterns = [
    # Authentication
    path('login/', user_login_view, name='login'),
    path('logout/', user_logout_view, name='logout'),
    path('password/change/', change_password, name='password-change'),
    path('password/change/done/', change_password_done, name='password-change-done'),

    # js validations
    path('ajax/validate/email/', validate_email_view, name='ajax-validate-email'),
    path('ajax/validate/email/<int:user_id>/update/', validate_email_update_view, name='ajax-validate-email-update'),
]    