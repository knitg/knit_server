from rest_framework import serializers
from users.models import User
from ..kmodels.image_model import KImage
from ..kmodels.address_model import KAddress
from ..kmodels.usertype_model import KUserType

from ..kmodels.profile_model import Profile

from django.db.models.signals import post_save

from .image_serializer import KImageSerializer
from .address_serializer import KAddressSerializer
from .usertype_serializer import KUserTypeSerializer


class CurrentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        # fields = ('id','url', 'username', 'email', 'phone', 'password',)
        fields = "__all__"

    def create(self, validated_data):
        ## Image data
        user = User.objects.create_user(**validated_data)
        user.save()
        return user 

    def update(self, instance, validated_data):
        user_data = {}
        instance.phone = self.initial_data.get('phone') if self.initial_data.get('phone') else instance.phone
        instance.email = self.initial_data.get('email') if self.initial_data.get('email') else instance.email
        instance.password = self.initial_data.get('password') if self.initial_data.get('password') else instance.password
        instance.username = self.initial_data.get('username') if self.initial_data.get('username') else instance.username
        instance.save()
        return instance    


# Function to Create user Profile
def create_profile_account(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
#Post Save handler to create user Account/Profile
post_save.connect(create_profile_account, sender=User, weak=False)