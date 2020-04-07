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
    user_id =  serializers.CharField(source="user.id", required=False)
    phone =  serializers.CharField(source="user.phone", required=False)
    email =  serializers.EmailField(source="user.email", required=False)
    # images = KImageSerializer(many=True, required=False, allow_null=True)
    userTypes = KUserTypeSerializer(source='user.profile.userTypes', many=True, required=False, allow_null=True) 
    
    
    class Meta:
        model = KVendorUser
        fields = [ 'id', 'name','user_id', 'phone', 'email', 'userTypes']
        # fields = ["id", "name", "user", 'open_time', 'close_time', 'masters_count', 'is_weekends', 'is_open', 'is_emergency_available', 'is_door_service', 'address']
        # fields = "__all__"


    def create(self, validated_data):
        users_data = self.initial_data.pop('user')
        validated_data = self.initial_data.pop('vendor')  
        # User creation
        user_serializer = UserSerializer(data=users_data, many=False)
        if user_serializer.is_valid():
            user_serializer.save()
        else:
            raise serializers.ValidationError("Something went wrong with user creation")

        # User profile get 
        profile = user_serializer.instance.profile
        # Vendor creation
        vendor = KVendorUser.objects.create(user=user_serializer.instance, **validated_data)
        
        if not (self.initial_data.get('data').get('userTypes') is None):
            userTypeIds = self.initial_data.get('data').get('userTypes').split(',')
            usertypes = list(KUserType.objects.filter(id__in=userTypeIds))
            profile.userTypes.set(usertypes)
            vendor.userTypes.set(usertypes)
            
        if (self.initial_data.get('data').get('userTypes') is None):
            # usertypes = list(KUserType.objects.filter(user_type__iexact='Customer'))
            usertypes = list(KUserType.objects.filter(id__in=['1']))
            profile.userTypes.set(usertypes)
            vendor.userTypes.set(usertypes)
        
        if not (self.initial_data.get('data').get('address') is None):
            addresses = self.initial_data.get('data').get('address').split(',')
            address = list(KAddress.objects.filter(id__in=addresses))
            profile.address.set(address)

        if not (self.initial_data.get('data').get('images') is None):
            image_data = self.initial_data.get('data')['images']
            for image in image_data:
                c_image= image_data[image]
                images = KImage.objects.create(image=c_image, description=self.initial_data.get('description'), source='user_'+str(user.id), size=c_image.size)
                vendor.images.add(images)  
                profile.images.add(usertypes)  
        
        return vendor
            
    def update(self, instance, validated_data):
        instance.name = self.initial_data.get('name') if self.initial_data.get('name') else instance.name
        instance.masters = self.initial_data.get('masters') if self.initial_data.get('masters') else instance.masters
        instance.openTime = self.initial_data.get('openTime') if self.initial_data.get('openTime') else instance.openTime
        instance.closeTime = self.initial_data.get('closeTime', None) if self.initial_data.get('closeTime', None) else instance.closeTime
        instance.closed = self.initial_data.get('closed') if self.initial_data.get('closed') else instance.closed
        instance.isWeekends = self.initial_data.get('isWeekends') if self.initial_data.get('isWeekends') else instance.isWeekends
        instance.doorService = self.initial_data.get('doorService') if self.initial_data.get('doorService') else instance.doorService
        instance.emergency = self.initial_data.get('emergency') if self.initial_data.get('emergency') else instance.emergency
        instance.description = self.initial_data.get('description') if self.initial_data.get('description') else instance.description

        if self.initial_data.get('address'):
            instance.address = self.initial_data.get('address', None) if self.initial_data.get('address', None) else instance.address
        user_data = {}
        if instance.user:
            user_data['phone'] = self.initial_data.get('phone', None) if self.initial_data.get('phone', None) else instance.user.phone
            user_data['email'] = self.initial_data.get('email', None) if self.initial_data.get('email', None) else instance.user.email
            user_data['password'] = self.initial_data.get('password', None) if self.initial_data.get('password', None) else instance.user.password
            user_data['username'] = self.initial_data.get('username', None) if self.initial_data.get('username', None) else instance.user.username
                
            user = User.objects.update_or_create(pk=instance.user.id, defaults=user_data)[0]
              
        if not (self.initial_data.get('userTypes') is None):
            userTypeIds = self.initial_data['userTypes'].split(',')
            usertypes = list(KUserType.objects.filter(id__in=userTypeIds))
            instance.userTypes.set(usertypes)
 
        if not (self.initial_data.get('images') is None):
            image_data = self.initial_data['images']
                ### Remove relational images if any ####
            for e in instance.user.images.all():
                instance.user.images.remove(e)
                KImage.objects.get(id=e.id).delete()
            for image in image_data:
                c_image= image_data[image]
                images = KImage.objects.create(image=c_image, description=self.initial_data.get('description'), source='user_'+str(user.id), size=c_image.size)
                instance.images.add(images)          

        instance.save() 
        return instance