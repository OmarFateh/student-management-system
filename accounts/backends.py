from django.contrib.auth.backends import ModelBackend

from .models import User

class EmailBackend(ModelBackend):
    """
    Authenticates against settings.AUTH_USER_MODEL.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        # Check the email and password of a user, and return a user.
        try:
            user = User.objects.filter(email__iexact=username).first()
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None


    def get_user(self, user_id):
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
        return user if self.user_can_authenticate(user) else None

        


        