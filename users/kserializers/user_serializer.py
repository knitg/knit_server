from rest_framework import serializers
from ..kmodels.user_model import User
from ..kmodels.image_model import KImage
from ..kmodels.usertype_model import KUserType

from .image_serializer import KImageSerializer
from .usertype_serializer import KUserTypeSerializer

class UserSerializer(serializers.HyperlinkedModelSerializer):
    images = KImageSerializer(many=True, required=False, allow_null=True)
    user_type = KUserTypeSerializer(many=True, required=False, allow_null=True) 
    class Meta:
        model = User
        fields = ('id', 'userName', 'email', 'phone', 'password', 'user_type', 'user_role', 'images')
         

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
        if self.initial_data.get('user_type') or user_type:
            user_types = self.initial_data['user_type'].split(',')
            usertypes = list(KUserType.objects.filter(id__in=user_types))
            user.user_type.set(usertypes)

        return user 

    def update(self, instance, validated_data):
        user_data = {}
        instance.phone = self.initial_data['phone'] if self.initial_data['phone'] else instance.phone
        instance.email = self.initial_data['email'] if self.initial_data['email'] else instance.email
        instance.password = self.initial_data['password'] if self.initial_data['password'] else instance.password
        instance.user_role = self.initial_data['user_role'] if self.initial_data['user_role'] else instance.user_role
        instance.userName = self.initial_data['userName'] if self.initial_data['userName'] else instance.userName
        
        if self.initial_data.get('user_type'):
            user_types = self.initial_data['user_type'].split(',')
            usertypes = list(KUserType.objects.filter(id__in=user_types))
            instance.user_type.set(usertypes)  

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


