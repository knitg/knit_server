from rest_framework import serializers
from ..kmodels.color_model import ColorModel

class ColorSerilizer(serializers.ModelSerializer):
    class Meta:
        model = ColorModel
        fields = ('id', 'color', 'code')
    
    def validate(self, data):
        if data.get('color'):
            data['code'] = data.get('color', '').replace(" ", "_").upper()
        else:
            raise serializers.ValidationError("Color is required")
        return data

    def create(self, validated_data):       
        ## Role data 
        color = ColorModel.objects.create(**validated_data)
        return color

    def update(self, instance, validated_data):
        # Update the Foo instance
        instance.color = validated_data.get('color', instance.color) 
        instance.code = validated_data.get('code', instance.code) 
        instance.save() 
        return instance