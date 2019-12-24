from django.conf import settings
from django.contrib.auth import get_user_model
import re

from django.contrib.auth.models import User
from django.db.models import Q


class EmailOrPhoneOrUsernameModelBackend(object):
    """
    This is a ModelBacked that allows authentication with either a username or an email address.

    """
    def authenticate(self, username=None, password=None):
        phoneNumber = re.search(r'\b[789]\d{9}\b', username, flags=0)

        if '@' in username:
            kwargs = {'email': username}
        elif phoneNumber:
            kwargs = {'phone': username.group(0)}
        else:
            kwargs = {'username': username}
        try:
            user = get_user_model().objects.get(**kwargs)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, username):
        try:
            return get_user_model().objects.get(pk=username)
        except get_user_model().DoesNotExist:
            return None


class EmailAuthenticate(object):

    def authenticate(self, username=None,email=None, phone=None,  password=None, **kwargs):
        try:
            user = get_user_model().objects.get(Q(email=email) | Q(phone=phone) | Q(username=username))
        except get_user_model().DoesNotExist:
            return None

        if user.check_password(password):
            return user
        return None

    def get_user(self,user_id):
        try:
            return get_user_model().objects.get(pk=user_id)
        except get_user_model().DoesNotExist:
            return None