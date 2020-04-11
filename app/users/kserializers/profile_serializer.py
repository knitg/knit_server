from rest_framework import serializers
from ..kmodels.image_model import KImage
from ..kmodels.profile_model import Profile
from ..kmodels.address_model import Address
from ..kmodels.usertype_model import UserType

from .image_serializer import KImageSerializer
from .usertype_serializer import UserTypeSerializer
from .address_serializer import AddressSerializer

class ProfileSerializer(serializers.ModelSerializer):  
    # getting user details
    userId = serializers.ReadOnlyField(source='user.id')
    username = serializers.ReadOnlyField(source='user.username')
    email = serializers.ReadOnlyField(source='user.email')
    phone = serializers.ReadOnlyField(source='user.phone')

    firstName = serializers.CharField(allow_blank=True, required=False)
    lastName = serializers.CharField(allow_blank=True, required=False)
    gender = serializers.IntegerField(required=False)
    married = serializers.BooleanField(required=False)
    # userTypeIds = serializers.PrimaryKeyRelatedField(many=True, read_only=False, queryset=UserType.objects.all(), source='userTypes')

    images = serializers.SerializerMethodField(read_only=True)
    userTypes = serializers.SerializerMethodField(read_only=True) 
    address = serializers.SerializerMethodField(read_only=True)

    def get_userTypes(self, obj):
        serializer = UserTypeSerializer(obj.userTypes, many=True)
        return serializer.data 

    def get_images(self, obj):
        serializer = KImageSerializer(obj.images, many=True)
        return serializer.data 
    
    def get_address(self, obj):
        serializer = AddressSerializer(obj.address, many=True)
        return serializer.data     
    
    class Meta:
        model = Profile
        depth = 1
        # fields = '__all__'
        fields = ("userId", "username", "email", "phone", "userTypes", "firstName", "lastName", "gender", "married", "images", "address", "is_active")

    def update(self, instance, validated_data):
        errors = []
        instance.firstName = self.initial_data.get('firstName', instance.firstName)
        instance.lastName = self.initial_data.get('lastName', instance.lastName)
        instance.gender = self.initial_data.get('gender', instance.gender)
        instance.married = self.initial_data.get('married', instance.married)
        instance.anniversary = self.initial_data.get('anniversary', instance.anniversary)
        if self.initial_data.get('images'):
            validated_data['images'] = self.initial_data['images']
            image_data = validated_data.pop('images')
            for image in image_data:
                c_image= image_data[image]
                images = KImage.objects.create(image=c_image, description=self.initial_data.get('description'), source='user_'+str(user.id), size=c_image.size)
                instance.images.add(images)
        
        if self.initial_data.get('userTypes') is not None:
            if isinstance(self.initial_data.get('userTypes'), list):
                usertypes = list(UserType.objects.filter(id__in=self.initial_data.get("userTypes")))
                instance.userTypes.set(usertypes)
            else:
                errors.append("User types expected an array")

        if self.initial_data.get('address'):
            if isinstance(self.initial_data.get('address'), list):
                address = list(Address.objects.filter(id__in=self.initial_data.get("address")))
                instance.address.set(address)
            else:
                errors.append("address ids should be list")
        if len(errors):
            raise serializers.ValidationError(errors)
        else:   
            instance.save() 
        return instance
    

