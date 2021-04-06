from django.urls import path

from .views import (
    add_session, 
    manage_session,
    paginate_session,
    update_session,
    delete_session,
    validate_session_view,
    validate_session_update_view
)        

# namespace = adminhod

urlpatterns = [
    # session
    path('sessions/add/', add_session, name='add-session'),
    path('sessions/', manage_session, name='manage-session'),
    path('ajax/session/paginate/', paginate_session, name='ajax-paginate-session'),
    path('sessions/<int:session_id>/update/', update_session, name='update-session'),
    path('sessions/<int:session_id>/delete/', delete_session, name='delete-session'),

    # js validations
    path('ajax/validate/session/', validate_session_view, name='ajax-validate-session'),
    path('ajax/validate/session/<int:session_id>/update/', validate_session_update_view, name='ajax-validate-session-update'),
] 