from rest_framework import serializers
from users.models import User
from ..kmodels.image_model import KImage
from ..kmodels.address_model import KAddress
from ..kmodels.usertype_model import KUserType

from .image_serializer import KImageSerializer
from .address_serializer import KAddressSerializer
from .usertype_serializer import KUserTypeSerializer


class CurrentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    images = KImageSerializer(many=True, required=False, allow_null=True)
    user_type = KUserTypeSerializer(many=True, required=False, allow_null=True) 
    address = KAddressSerializer(many=True, required=False, allow_null=True) 
    class Meta:
        model = User
        fields = ('id','url', 'username', 'email', 'phone', 'password', 'user_type', 'user_role', 'images', 'address')
         

    def create(self, validated_data):
        ## Image data
        user = User.objects.create_user(**validated_data)
        user.save()
        if self.initial_data.get('images'):
            validated_data['images'] = self.initial_data['images']
            image_data = validated_data.pop('images')
            for image in image_data:
                c_image= image_data[image]
                images = KImage.objects.create(image=c_image, description=self.initial_data.get('description'), source='user_'+str(user.id), size=c_image.size)
                user.images.add(images)
        if self.initial_data.get('user_type'):
            user_types = self.initial_data['user_type'].split(',')
            usertypes = list(KUserType.objects.filter(id__in=user_types))
            user.user_type.set(usertypes)

        if self.initial_data.get('address'):
            addresses = self.initial_data['address'].split(',')
            address = list(KAddress.objects.filter(id__in=addresses))
            user.address.set(address)

        return user 

    def update(self, instance, validated_data):
        user_data = {}
        instance.phone = self.initial_data.get('phone') if self.initial_data.get('phone') else instance.phone
        instance.email = self.initial_data.get('email') if self.initial_data.get('email') else instance.email
        instance.password = self.initial_data.get('password') if self.initial_data.get('password') else instance.password
        instance.user_role = self.initial_data.get('user_role') if self.initial_data.get('user_role') else instance.user_role
        instance.username = self.initial_data.get('username') if self.initial_data.get('username') else instance.username
        
        if self.initial_data.get('user_type'):
            user_types = self.initial_data['user_type'].split(',')
            usertypes = list(KUserType.objects.filter(id__in=user_types))
            instance.user_type.set(usertypes)  
    
        if self.initial_data.get('address'):
            addresses = self.initial_data['address'].split(',')
            address = list(KAddress.objects.filter(id__in=addresses))
            instance.address.set(address)

        if self.initial_data.get('images'):
            image_data = self.initial_data['images']
            ### Remove relational images if any ####
            for e in instance.images.all():
                instance.images.remove(e)
                KImage.objects.get(id=e.id).delete()
            for image in image_data:
                c_image= image_data[image]
                images = KImage.objects.create(image=c_image, description=self.initial_data.get('description'), source='user_'+str(instance.id), size=c_image.size)
                instance.images.add(images) 

        instance.save()
        return instance    

