from rest_framework import serializers
from users.models import User
from ..kmodels.image_model import KImage
from ..kmodels.address_model import KAddress
from ..kmodels.customer_model import KCustomer
from ..kmodels.vendor_model import KVendorUser
from ..kmodels.usertype_model import KUserType

from .image_serializer import KImageSerializer
from .usertype_serializer import KUserTypeSerializer
from .user_serializer import UserSerializer

class KVendorUserSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer(many=False)    
    class Meta:
        model = KVendorUser
        # fields = [ 'name','user', 'address']
        # fields = ["id", "name", "user", 'open_time', 'close_time', 'masters_count', 'is_weekends', 'is_open', 'is_emergency_available', 'is_door_service', 'address']
        fields = "__all__"
    def create(self, validated_data):
        users_data = self.initial_data.pop('user')
        validated_data = self.initial_data.pop('vendor')    
        
        user = User.objects.create_user(**users_data)
        user.save()
        if self.initial_data.get('data')['user_type']:
            user_types = self.initial_data.get('data')['user_type'].split(',')
            usertypes = list(KUserType.objects.filter(id__in=user_types))
            user.user_type.set(usertypes)
            
        if self.initial_data.get('data')['address']:
            addresses = self.initial_data.get('data')['address'].split(',')
            address = list(KAddress.objects.filter(id__in=addresses))
            user.address.set(address)

        if self.initial_data.get('data')['images']:
            image_data = self.initial_data.get('data')['images']
            for image in image_data:
                c_image= image_data[image]
                images = KImage.objects.create(image=c_image, description=self.initial_data.get('description'), source='user_'+str(user.id), size=c_image.size)
                user.images.add(images)

        vendor = KVendorUser.objects.create(user=user, **validated_data)
        return vendor
            
    def update(self, instance, validated_data):
        instance.name = validated_data['name'] if validated_data['name'] else instance.name
        instance.masters_count = validated_data['masters_count'] if validated_data['masters_count'] else instance.masters_count
        instance.open_time = self.initial_data['open_time'] if self.initial_data.get('open_time') else instance.open_time
        instance.close_time = self.initial_data.get('close_time', None) if self.initial_data.get('close_time', None) else instance.close_time
        instance.is_open = validated_data['is_open'] if validated_data['is_open'] else instance.is_open
        instance.is_weekends = validated_data['is_weekends'] if validated_data['is_weekends'] else instance.is_weekends
        instance.is_door_service = validated_data['is_door_service'] if validated_data['is_door_service'] else instance.is_door_service
        instance.is_emergency_available = validated_data['is_emergency_available'] if validated_data['is_emergency_available'] else instance.is_emergency_available

        if self.initial_data.get('address'):
            instance.address = self.initial_data.get('address', None) if self.initial_data.get('address', None) else instance.address
        user_data = {}
        if instance.user:
            user_data['phone'] = self.initial_data.get('phone', None) if self.initial_data.get('phone', None) else instance.user.phone
            user_data['email'] = self.initial_data.get('email', None) if self.initial_data.get('email', None) else instance.user.email
            user_data['password'] = self.initial_data.get('password', None) if self.initial_data.get('password', None) else instance.user.password
            user_data['username'] = self.initial_data.get('username', None) if self.initial_data.get('username', None) else instance.user.username
                
            user = User.objects.update_or_create(pk=instance.user.id, defaults=user_data)[0]
            if not (self.initial_data.get('user_type') is None):
                user_types = self.initial_data['user_type'].split(',')
                usertypes = list(KUserType.objects.filter(id__in=user_types))
                user.user_type.set(usertypes)

            if not (self.initial_data.get('address') is None):
                addresses = self.initial_data.get('address').split(',')
                address = list(KAddress.objects.filter(id__in=addresses))
                user.address.set(address)

            if not (self.initial_data.get('images') is None):
                image_data = self.initial_data['images']
                 ### Remove relational images if any ####
                for e in instance.user.images.all():
                    instance.user.images.remove(e)
                    KImage.objects.get(id=e.id).delete()
                for image in image_data:
                    c_image= image_data[image]
                    images = KImage.objects.create(image=c_image, description=self.initial_data.get('description'), source='user_'+str(user.id), size=c_image.size)
                    user.images.add(images)            

        instance.save() 
        return instance    