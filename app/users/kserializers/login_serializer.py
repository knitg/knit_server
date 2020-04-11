from django.contrib.auth import get_user_model, authenticate
from django.conf import settings
from rest_framework import serializers, exceptions
from rest_framework.exceptions import ValidationError
from users.models import User
from ..kmodels.image_model import KImage
from ..kmodels.address_model import Address
from ..kmodels.usertype_model import UserType
import types
from ..kmodels.profile_model import Profile

from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save

from .image_serializer import KImageSerializer
from .address_serializer import AddressSerializer
from .usertype_serializer import UserTypeSerializer

UserModel = get_user_model()

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    phone = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(style={'input_type': 'password'})
    
    def get_fields(self):
        fields = super(LoginSerializer, self).get_fields()
        # fields['email'] = fields['username']
        fields['phone'] = fields['username']
        del fields['username']
        return fields

    def authenticate(self, **kwargs):
        return authenticate(self.context['request'], **kwargs)
    
    def _validate_phone(self, phone, password):
        user = None

        if phone and password:
            user = self.authenticate(phone=phone, password=password)
        else:
            msg = _('Must include "phone" and "password".')
            raise exceptions.ValidationError(msg)

        return user

    def _validate_email(self, email, password):
        user = None

        if email and password:
            user = self.authenticate(email=email, password=password)
        else:
            msg = _('Must include "email" and "password".')
            raise exceptions.ValidationError(msg)

        return user

    def _validate_username(self, username, password):
        user = None

        if username and password:
            user = self.authenticate(username=username, password=password)
        else:
            msg = _('Must include "username" and "password".')
            raise exceptions.ValidationError(msg)

        return user

    def validate(self, attrs):
        username = self.initial_data.get('username')  
        email = attrs.get('email')
        password = attrs.get('password')
        phone = attrs.get('phone')

        user = None

        if 'allauth' in settings.INSTALLED_APPS:
            from allauth.account import app_settings

            # Authentication through email
            # if app_settings.AUTHENTICATION_METHOD == app_settings.AuthenticationMethod.EMAIL:
            if email is not None:
                user = self._validate_email(email, password)

            # Authentication through username
            # elif app_settings.AUTHENTICATION_METHOD == app_settings.AuthenticationMethod.USERNAME:
            elif username is not None:    
                user = self._validate_username(username, password)

            # Authentication through phone
            else:
                user = self._validate_phone(phone, password)

        else:
            # Authentication without using allauth
            if email:
                try:
                    username = UserModel.objects.get(email__iexact=email).get_username()
                except UserModel.DoesNotExist:
                    pass

            if username:
                user = self._validate_username_email(username, '', password)

        # Did we get back an active user?
        if user:
            if not user.is_active:
                msg = _('User account is disabled.')
                raise exceptions.ValidationError(msg)
        else:
            msg = _('Unable to log in with provided credentials or not active user.')
            raise exceptions.ValidationError(msg)

        # If required, is the email verified?
        if 'rest_auth.registration' in settings.INSTALLED_APPS:
            from allauth.account import app_settings
            if app_settings.EMAIL_VERIFICATION == app_settings.EmailVerificationMethod.MANDATORY:
                email_address = user.emailaddress_set.get(email=user.email)
                if not email_address.verified:
                    raise serializers.ValidationError(_('E-mail is not verified.'))

        attrs['user'] = user
        return attrs