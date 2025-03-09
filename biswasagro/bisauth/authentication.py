from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import check_password
from .models import Usersinfo


class UsersInfoBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = Usersinfo.objects.get(username=username)
            if check_password(password, user.password):
                return user
        except Usersinfo.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Usersinfo.objects.get(pk=user_id)
        except Usersinfo.DoesNotExist:
            return None
