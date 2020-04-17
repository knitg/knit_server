from rest_framework import serializers
from ..kmodels.sizes_model import SizeModel

class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SizeModel
        fields = ('id', 'size')
    
    def validate(self, data):
        if data.get('size'):
            data['code'] = data.get('size', '').replace(" ", "_").upper()
        else:
            raise serializers.ValidationError("Size is required")
        return data

    def create(self, validated_data):       
        ## Role data 
        size = SizeModel.objects.create(**validated_data)
        return size

    def update(self, instance, validated_data):
        # Update the Foo instance
        instance.size = validated_data.get('size', instance.size) 
        instance.code = validated_data.get('code', instance.code) 
        instance.save() 
        return instance