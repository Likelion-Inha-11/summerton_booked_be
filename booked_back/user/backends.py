from django.contrib.auth.backends import BaseBackend
from .models import Profile

class YourCustomBackend(BaseBackend):
    def authenticate(self, request, userID=None, password=None, **kwargs):
        try:
            user = Profile.objects.get(userID=userID)
            if user.check_password(password):
                return user
        except Profile.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Profile.objects.get(pk=user_id)
        except Profile.DoesNotExist:
            return None
