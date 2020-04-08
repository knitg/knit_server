from rest_framework import serializers
from users.models import User
from ..kmodels.image_model import KImage
from ..kmodels.profile_model import Profile
from ..kmodels.address_model import KAddress
from ..kmodels.vendor_model import KVendorUser
from ..kmodels.usertype_model import KUserType

from .profile_serializer import KProfileSerializer
from .image_serializer import KImageSerializer
from .usertype_serializer import KUserTypeSerializer
from .user_serializer import UserSerializer

class KVendorUserSerializer(serializers.ModelSerializer):
    # user = UserSerializer(many=False) 
    user_id =  serializers.IntegerField(source="user.id", required=False)
    phone =  serializers.CharField(source="user.phone", required=False)
    email =  serializers.EmailField(source="user.email", required=False)
    fullName =  serializers.EmailField(source="user.profile.get_full_name", required=False)
    # images = KImageSerializer(many=True, required=False, allow_null=True)
    userTypes = KUserTypeSerializer(source='user.profile.userTypes', many=True, required=False, allow_null=True) 
    
    
    class Meta:
        model = KVendorUser
        fields = [ 'id', 'name','user_id', 'phone', 'email', 'userTypes', 'fullName']
        # fields = ["id", "name", "user", 'open_time', 'close_time', 'masters_count', 'is_weekends', 'is_open', 'is_emergency_available', 'is_door_service', 'address']
        
    def create(self, validated_data):
        users_data = self.initial_data.pop('user')  
        validated_data = self.initial_data.pop('vendor')  
        # User creation
        user_serializer = UserSerializer(data=users_data, many=False)
        if user_serializer.is_valid():
            user_serializer.save()
        else:
            raise serializers.ValidationError("Something went wrong with user creation")
        # Vendor creation
        vendor = KVendorUser.objects.create(user=user_serializer.instance, **validated_data)
        return vendor
            
    def update(self, instance, validated_data):
        userObj = self.initial_data.get('user')
        vendorObj = self.initial_data.get('vendor')
        self.updateUserData(userObj, instance)
        updated_instance = self.updateVendorData(vendorObj, instance)
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
        if user_info['profile'].get('userTypes') is not None:
            userTypeIds = user_info['profile'].get('userTypes', '').split(',')
            usertypes = list(KUserType.objects.filter(id__in=userTypeIds))
            instance.user.profile.userTypes.set(usertypes)
        if user_info['profile'].get('address') is not None:
            addressIds = str(user_info['profile'].get('address', '')).split(',')
            addresses = list(KAddress.objects.filter(id__in=addressIds))
            instance.user.profile.address.set(addresses)
            
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

