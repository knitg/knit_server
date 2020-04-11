from rest_framework import serializers
from ..kmodels.usertype_model import UserType

class UserTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserType
        fields = ['id', 'user_type']

    def create(self, validated_data):       
        ## Role data 
        userType = UserType.objects.create(**validated_data)
        return userType

    def update(self, instance, validated_data):
        # Update the Foo instance
        instance.user_type = validated_data.get('user_type', instance.user_type) 
        instance.description = validated_data.get('description', instance.description) 
        instance.save() 
        return instance