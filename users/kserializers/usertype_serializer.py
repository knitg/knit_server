from rest_framework import serializers
from ..kmodels.usertype_model import KUserType

class KUserTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = KUserType
        fields = "__all__"

    def create(self, validated_data):       
        ## Role data 
        userType = KUserType.objects.create(**validated_data)
        return userType

    def update(self, instance, validated_data):
        # Update the Foo instance
        instance.user_type = validated_data['user_type'] 
        instance.description = validated_data['description'] 
        instance.save() 
        return instance