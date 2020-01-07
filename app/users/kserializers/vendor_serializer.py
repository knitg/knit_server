from rest_framework import serializers
from users.models import User
from ..kmodels.image_model import KImage
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
        fields = ["id", "name", "user"]

    def create(self, validated_data):
        users_data = self.initial_data.pop('user')
        validated_data = self.initial_data.pop('vendor')    
        
        user = User.objects.create_user(**users_data)
        user.save()
        if self.initial_data.get('data')['user_type']:
            user_types = self.initial_data.get('data')['user_type'].split(',')
            usertypes = list(KUserType.objects.filter(id__in=user_types))
            user.user_type.set(usertypes)
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
        if instance.address and self.initial_data['address']:
            instance.address = self.initial_data['address'] if self.initial_data['address'] else instance.address
        user_data = {}
        if instance.user:
            user_data['phone'] = self.initial_data['phone'] if self.initial_data['phone'] else instance.user.phone
            user_data['email'] = self.initial_data['email'] if self.initial_data['email'] else instance.user.email
            user_data['password'] = self.initial_data['password'] if self.initial_data['password'] else instance.user.password
            user_data['user_role'] = self.initial_data['user_role'] if self.initial_data['user_role'] else instance.user.user_role
            user_data['username'] = self.initial_data['username'] if self.initial_data['username'] else instance.user.username
            
            user = User.objects.update_or_create(pk=instance.user.id, defaults=user_data)[0]
            if self.initial_data.get('user_type'):
                user_types = self.initial_data['user_type'].split(',')
                usertypes = list(KUserType.objects.filter(id__in=user_types))
                user.user_type.set(usertypes)

            if self.initial_data.get('images'):
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