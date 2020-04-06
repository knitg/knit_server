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

import re

class CurrentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']


class UserSerializer(serializers.ModelSerializer):
    
    fullName = serializers.CharField(source='profile.get_full_name', required=False)
    # image = serializers.CharField(source='profile.get_default_image', required=False)
    # username = serializers.CharField(required=False)
    # email = serializers.EmailField(required=False)
    # phone = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'phone', 'fullName',)

    def validate_phone(self, value):
        phoneNumber = re.search(r'\b[6789]\d{9}\b', value)
        if len(value) > 10:
            raise serializers.ValidationError('Phone length should be 10 numbers')
        if phoneNumber is None:
            raise serializers.ValidationError('Phone number should starts with 6,7,8,9 number')
        
        ## Check if phone number already registered
        hasPhoneNumbers = User.objects.filter(phone=value)
        if len(hasPhoneNumbers):
            raise serializers.ValidationError('Phone number should be unique')
        
        return value

    def validate_username(self, value):
        if re.search(r"\s", value):
            raise serializers.ValidationError("user name shouldn't have spaces")
        return value

    def validate_email(self, value):
        ## Check if email already registered
        isEmailExists = User.objects.filter(email=value)
        if len(isEmailExists):
            raise serializers.ValidationError('email already exists')
        return value
    

    def validate(self, data):
        if data.get('email') is None and data.get('phone') is None and data.get('username') is None:
            raise serializers.ValidationError("Email or phone required")
        if data.get('username') is None:
            data['username'] = data.get('username', None)
        if data.get('email') is None:
            data['email'] = data.get('email', None)
        if data.get('phone') is None:
            data['phone'] = data.get('phone', None)
        if self.initial_data.get('password') is None:
            raise serializers.ValidationError("password is required")
        else:
            data['password'] = self.initial_data.get('password')
        return data

    ### USING BELOW METHOD CHECKING ADMIN USER
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.is_superuser:
            representation['admin'] = True
        if hasattr(instance, 'kvendoruser'):
            representation['vendor_id'] = instance.kvendoruser.id
        return representation


    def create(self, validated_data):
        # pass
        ## Image data
        self.hasAccountErrors = []
        user = User.objects.create_user(**validated_data)

        if self.initial_data.get('userTypes'):
            userTypeIds = self.initial_data['userTypes'].split(',')
            if not ('1' in userTypeIds):
                kvendoruser = KVendorUser.objects.create(user=user)
                kvendoruser.save()

        user.save()

        
        ## PROFILE MODEL CREATES
        profile = user.profile
        profile.firstName = self.initial_data.get('firstName', profile.firstName)
        profile.lastName = self.initial_data.get('lastName', profile.lastName)
        profile.gender = self.initial_data.get('gender', profile.gender)
        profile.married = self.initial_data.get('married', profile.married)
        profile.birthday = self.initial_data.get('birthday', profile.birthday)
        profile.anniversary = self.initial_data.get('anniversary', profile.anniversary)
        profile.user_role = self.initial_data.get('user_role', profile.user_role)
        
        if self.initial_data.get('userTypes'):
            userTypeIds = self.initial_data['userTypes'].split(',')
            usertypes = list(KUserType.objects.filter(id__in=userTypeIds))
            profile.userTypes.set(usertypes)

        if type(self.initial_data.get('address')) is str :
            addresses = self.initial_data['address'].split(',')
            address = list(KAddress.objects.filter(id__in=addresses))
            profile.address.set(address)

        profile.save()


        return user 

    def update(self, instance, validated_data):
        
        profile_data = self.initial_data.pop('userProfile')

        instance.phone = self.initial_data.get('phone') if self.initial_data.get('phone') else instance.phone
        instance.email = self.initial_data.get('email') if self.initial_data.get('email') else instance.email
        instance.password = self.initial_data.get('password') if self.initial_data.get('password') else instance.password
        instance.username = self.initial_data.get('username') if self.initial_data.get('username') else instance.username
        
        instance.save()
        # get and update user profile
        profile = instance.profile
        if profile_data:
            profile.firstName = profile_data.get('firstName') if profile_data.get('firstName') else profile.firstName
            profile.lastName = profile_data.get('lastName') if profile_data.get('lastName') else profile.lastName
            profile.gender = profile_data.get('gender') if profile_data.get('gender') else profile.gender
            profile.married = profile_data.get('married') if profile_data.get('married') else profile.married
            profile.birthday = profile_data.get('birthday') if profile_data.get('birthday') else profile.birthday
            profile.anniversary = profile_data.get('anniversary') if profile_data.get('anniversary') else profile.anniversary
            profile.user_role = profile_data.get('user_role') if profile_data.get('user_role') else profile.user_role
            
            if profile_data.get('userTypes'):
                userTypeIds = profile_data['userTypes'].split(',')
                usertypes = list(KUserType.objects.filter(id__in=userTypeIds))
                profile.userTypes.set(usertypes)

            if type(profile_data.get('address')) is str :
                addresses = profile_data['address'].split(',')
                address = list(KAddress.objects.filter(id__in=addresses))
                instance.address.set(address)

            profile.save()
        return instance


# Function to Create user Profile
def create_profile_account(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
#Post Save handler to create user Account/Profile
post_save.connect(create_profile_account, sender=User, weak=False)