from rest_framework import serializers
from ..kmodels.material_model import MaterialModel

class MaterialSerilizer(serializers.ModelSerializer):
    class Meta:
        model = MaterialModel
        fields = ('id', 'material', 'code')
    
    def validate(self, data):
        if data.get('material'):
            data['material'] = data.get('color', '').replace(" ", "_").upper()
        else:
            raise serializers.ValidationError("Material is required")
        return data

    def create(self, validated_data):       
        ## Role data 
        material = MaterialModel.objects.create(**validated_data)
        return material

    def update(self, instance, validated_data):
        # Update the Foo instance
        instance.material = validated_data.get('material', instance.material) 
        instance.code = validated_data.get('code', instance.code) 
        instance.save() 
        return instance