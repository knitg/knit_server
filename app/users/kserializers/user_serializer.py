from rest_framework import serializers
from users.models import User
from ..kmodels.image_model import KImage
from ..kmodels.address_model import KAddress
from ..kmodels.usertype_model import KUserType
from ..kmodels.vendor_model import KVendorUser

import types
from ..kmodels.profile_model import Profile

from django.db.models.signals import post_save

from .image_serializer import KImageSerializer
from .address_serializer import KAddressSerializer
from .usertype_serializer import KUserTypeSerializer
from .profile_serializer import KProfileSerializer

import re

class CurrentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']


class UserSerializer(serializers.ModelSerializer):
    fullName = serializers.ReadOnlyField(source='profile.get_full_name', required=False)
    # password = serializers.CharField(required=False, max_length=105, style={'input_type': 'password'})
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'phone',  'fullName')
    
    def create(self, validated_data):
        validated_data = self.initial_data.get('user')
        user = User.objects.create_user(**validated_data)
        user.save()

        # ------ PROFILE CREATE ------ #
        profile = user.profile
        profile_data = self.initial_data.pop('profile')  
        self.profile_save(profile, profile_data)

        return user 

    def update(self, instance, validated_data):        
        users_data = self.initial_data.pop('user')
        instance.phone = users_data.get('phone', instance.phone)
        instance.email = users_data.get('email', instance.email)
        instance.username = users_data.get('username', instance.username)
        instance.is_admin = users_data.get('is_admin', instance.is_admin)
        instance.save()
        
        ## PROFILE MODEL CREATES
        profile = instance.profile
        profile_data = self.initial_data.get('profile')
        self.profile_save(profile, profile_data)

        return instance
    
    # ---=================== PROFILE DATA SAVE HERE ==========================--- #
    def profile_save(self, profile, profile_data):
        if profile_data is not None:
            profile.firstName = profile_data.get('firstName', profile.firstName)
            profile.lastName = profile_data.get('lastName', profile.lastName)
            profile.gender = profile_data.get('gender', profile.gender)
            profile.married = profile_data.get('married', profile.married)
            profile.birthday = profile_data.get('birthday', profile.birthday)
            profile.anniversary = profile_data.get('anniversary', profile.anniversary)
            profile.user_role = profile_data.get('user_role', profile.user_role)
        
            if profile_data.get('userTypes') is not None:
                userTypeIds = profile_data.get('userTypes', '').split(',')
                usertypes = list(KUserType.objects.filter(id__in=userTypeIds))
                profile.userTypes.set(usertypes)

            if type(profile_data.get('address')) is str :
                addresses = profile_data.get('address', '').split(',')
                address = list(KAddress.objects.filter(id__in=addresses))
                profile.address.set(address)

            profile.save()


    # ---=================== USER VALIDATIONS START HERE ==========================--- #
    #     
    def validate_phone(self, value):
        if value:
            phoneNumber = re.search(r'\b[6789]\d{9}\b', value)
            if len(value) > 10:
                raise serializers.ValidationError('Phone length should be 10 numbers')
            if phoneNumber is None:
                raise serializers.ValidationError('Phone number should starts with 6,7,8,9 number')
            
            ## Check if phone number already registered
            if self.instance is None:
                hasPhoneNumbers = User.objects.filter(phone=value)
                if len(hasPhoneNumbers):
                    raise serializers.ValidationError('Phone number should be unique')
        
        return value

    def validate_username(self, value):
        if value and re.search(r"\s", value):
            raise serializers.ValidationError("user name shouldn't have spaces")
        return value

    def validate_email(self, value):
        ## Check if email already registered
        if value and self.instance is None:
            isEmailExists = User.objects.filter(email=value)
            if len(isEmailExists):
                raise serializers.ValidationError('email already exists')
        return value
    

    def validate(self, data):
        data = self.initial_data.get('data')
        self.validate_username(data['username'])
        self.validate_email(data['email'])
        self.validate_phone(data['phone'])
        if data.get('email') is None and data.get('phone') is None and data.get('username') is None:
            raise serializers.ValidationError("Email or phone required")
        if data.get('username'):
            data['username'] = data.get('username', None)
        if data.get('email'):
            data['email'] = data.get('email', None)
        if data.get('phone'):
            data['phone'] = data.get('phone', None)
        if data.get('password') is None and self.instance is None:
            raise serializers.ValidationError("password is required")
        else:
            data['password'] = data.get('password')
        return data

    # USING BELOW METHOD CHECKING ADMIN USER
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.is_superuser:
            representation['admin'] = True
        if hasattr(instance, 'kvendoruser'):
            representation['vendor_id'] = instance.kvendoruser.id
        return representation
        
    # ---=================== USER VALIDATIONS END HERE ==========================--- #
    #     
    
# Function to Create user Profile
def create_profile_account(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
#Post Save handler to create user Account/Profile
post_save.connect(create_profile_account, sender=User, weak=False)