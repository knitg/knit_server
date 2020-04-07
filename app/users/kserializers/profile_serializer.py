from rest_framework import serializers
from ..kmodels.image_model import KImage
from ..kmodels.profile_model import Profile
from ..kmodels.address_model import KAddress
from ..kmodels.usertype_model import KUserType

from .image_serializer import KImageSerializer
from .usertype_serializer import KUserTypeSerializer
from .user_serializer import UserSerializer
from .address_serializer import KAddressSerializer

class KProfileSerializer(serializers.ModelSerializer):  
    # getting user details
    username = serializers.CharField(source='user.username')
    email = serializers.CharField(source='user.email')
    phone = serializers.CharField(source='user.phone')

    firstName = serializers.CharField(allow_blank=True, required=False)
    lastName = serializers.CharField(allow_blank=True, required=False)
    gender = serializers.IntegerField(required=False)
    married = serializers.BooleanField(required=False)
    userTypeIds = serializers.PrimaryKeyRelatedField(many=True, read_only=False, queryset=KUserType.objects.all(), source='userTypes')

    images = KImageSerializer(many=True, required=False, allow_null=True)
    userTypes = KUserTypeSerializer(many=True, required=False, allow_null=True) 
    address = KAddressSerializer(many=True, required=False, allow_null=True)
    full_address = serializers.CharField(read_only=True)

    class Meta:
        model = Profile
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.firstName = validated_data['firstName'] if validated_data['firstName'] else instance.firstName
        instance.lastName = validated_data['lastName'] if validated_data['lastName'] else instance.lastName
        instance.gender = self.initial_data['gender'] if self.initial_data.get('gender') else instance.gender
        
        if self.initial_data.get('images'):
            validated_data['images'] = self.initial_data['images']
            image_data = validated_data.pop('images')
            for image in image_data:
                c_image= image_data[image]
                images = KImage.objects.create(image=c_image, description=self.initial_data.get('description'), source='user_'+str(user.id), size=c_image.size)
                instance.images.add(images)
        
        if self.initial_data.get('userTypes'):
            userTypeIds = self.initial_data['userTypes'].split(',')
            usertypes = list(KUserType.objects.filter(id__in=userTypeIds))
            instance.userTypes.set(usertypes)

        if self.initial_data.get('address'):
            addresses = self.initial_data['address'].split(',')
            address = list(KAddress.objects.filter(id__in=addresses))
            instance.address.set(address)
        instance.save() 
        return instance
    

