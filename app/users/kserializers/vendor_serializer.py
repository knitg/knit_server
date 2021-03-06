from rest_framework import serializers
from users.models import User
from ..kmodels.image_model import KImage
from ..kmodels.profile_model import Profile
from ..kmodels.address_model import Address
from ..kmodels.vendor_model import Vendor
from ..kmodels.usertype_model import UserType
import datetime
from .profile_serializer import ProfileSerializer
from .image_serializer import KImageSerializer
from .usertype_serializer import UserTypeSerializer
from .address_serializer import AddressSerializer
from .user_serializer import UserSerializer

import logging
logger = logging.getLogger(__name__)

class VendorSerializer(serializers.ModelSerializer):
    # user = UserSerializer(many=False) 
    
    user_id =  serializers.IntegerField(source="user.id", required=False)
    phone =  serializers.CharField(source="user.phone", required=False)
    email =  serializers.EmailField(source="user.email", required=False)
    fullName =  serializers.EmailField(source="user.profile.get_full_name", required=False)
    # images = KImageSerializer(many=True, required=False, allow_null=True)
    address = serializers.SerializerMethodField(read_only=True)
    userTypes = serializers.SerializerMethodField(read_only=True)
     
    openTime = serializers.TimeField(format='%I:%M:%S %p', input_formats='%I:%M:%S %p', required=False)
    closeTime = serializers.TimeField(format='%I:%M:%S %p', input_formats='%I:%M:%S %p', required=False)
     
    
    def get_address(self, obj):
        serializer = AddressSerializer(obj.address, many=True)
        return serializer.data

    def get_userTypes(self, obj):
        serializer = UserTypeSerializer(obj.userTypes, many=True)
        return serializer.data    

    class Meta:
        model = Vendor
        fields = [ 'id', 'name','user_id', 'phone', 'email', 'fullName', "openTime", 'closeTime', 'userTypes', 'address']
        # fields = ["id", "name", "user", 'open_time', 'close_time', 'masters_count', 'is_weekends', 'is_open', 'is_emergency_available', 'is_door_service', 'address']
    
    def validate(self, data):
        data = self.initial_data.get('data')
        if data.get('name') is None:
            raise serializers.ValidationError("Name field is required")
        return data

    def create(self, validated_data):
        address_data = {}
        usertype_data = {}
        users_data = self.initial_data.pop('user')  
        validated_data = self.initial_data.pop('vendor')
        if validated_data.get("address"):
            address_data = validated_data.pop("address")
        if validated_data.get("userTypes"):
            usertype_data = validated_data.pop("userTypes")

        # User creation
        logger.info("User create initiated from vendor")
        user_serializer = UserSerializer(data={'user': users_data, 'profile': users_data.get('profile'), 'data':users_data}, many=False)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()
        logger.info("User created successfully")

        # Vendor creation
        vendor = Vendor.objects.create(user=user_serializer.instance, **validated_data)
        if address_data:
            if isinstance(address_data, list):
                address = list(Address.objects.filter(id__in=address_data))
                vendor.address.set(address)

            elif isinstance(address_data, str):
                arr = address_data.split(",")
                addr = list(Address.objects.filter(id__in=arr))
                vendor.address.set(addr)

            else:
                logger.warning("NOT SAVED ADDRESS TO PROFILE : Expected Address ids should be an array {}".format(type(address_data)))
        
        if usertype_data is not None:
            if isinstance(usertype_data, list):
                usertypes = list(UserType.objects.filter(id__in=usertype_data))
                instance.userTypes.set(usertypes)
            elif isinstance(usertype_data, str):
                arr = usertype_data.split(",")
                addr = list(UserType.objects.filter(id__in=arr))
                vendor.userTypes.set(addr)

            else:
                logger.warning("NOT SAVED USERTYPES : Expected usertype ids should be an array {}".format(type(usertype_data)))
                
        return vendor
            
    def update(self, instance, validated_data):
        userObj = self.initial_data.get('user')
        vendorObj = self.initial_data.get('vendor')
        self.updateUserData(userObj, instance)
        updated_instance = self.updateVendorData(vendorObj, instance)
        logger.info(updated_instance)
        logger.info("Vendor updated successfully")
        return updated_instance
    
#-------------------------------  UPDATE USER DATA --------------------------------#

    def updateUserData(self, user_info, instance):
        user_data = {}
        if user_info:
            instance.user.phone = user_info.get('phone', instance.user.phone)
            instance.user.email = user_info.get('email', instance.user.email)
            instance.user.username = user_info.get('username', instance.user.username)
            instance.user.profile.firstName = user_info['profile'].get('firstName', instance.user.profile.firstName)
            instance.user.profile.lastName = user_info['profile'].get('lastName', instance.user.profile.lastName)
            instance.user.profile.user_role = user_info['profile'].get('user_role', instance.user.profile.user_role)
        instance.user.save()
        instance.user.profile.save()
        if user_info['profile'].get('userTypes'):
            if isinstance(user_info['profile'].get('userTypes'), list):
                usertypes = list(UserType.objects.filter(id__in=user_info['profile'].get('userTypes')))
                instance.user.profile.userTypes.set(usertypes)
            else:
                logger.warning("NOT SAVED USERTYPES TO PROFILE : Expected UserType ids should be an array bug got a {} ".format(type(user_info['profile'].get('userTypes'))))

        if user_info['profile'].get('address'):
            if isinstance(user_info['profile'].get('address'), list):
                address = list(Address.objects.filter(id__in=user_info['profile'].get('address')))
                instance.user.profile.address.set(addresses)

            else:
                logger.warning("NOT SAVED ADDRESS TO PROFILE : Expected Address ids should be an array {}".format(type(profile_data.get('address'))))
                
#-------------------------------  UPDATE VENDOR DATA --------------------------------#

    def updateVendorData(self, vendor_info, instance):
        instance.name = vendor_info.get('name', instance.name)
        instance.openTime = vendor_info.get('openTime', instance.openTime)
        instance.closeTime = vendor_info.get('closeTime', instance.closeTime)
        instance.masters = vendor_info.get('masters', instance.masters)
        instance.isWeekends = vendor_info.get('isWeekends', instance.isWeekends)
        instance.alternateDays = vendor_info.get('alternateDays', instance.alternateDays)
        instance.closed = vendor_info.get('closed', instance.closed)
        instance.doorService = vendor_info.get('doorService', instance.doorService)
        instance.emergency = vendor_info.get('emergency', instance.emergency)
        instance.save()
        return instance

