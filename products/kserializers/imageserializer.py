from rest_framework import serializers
from ..kmodels.imagemodel import KImage


class KImageSerializer(serializers.HyperlinkedModelSerializer):  
    class Meta:
        model = KImage
        fields = ('id', 'image','description')
        # fields = '__all__'

    def create(self, validated_data):
        mydata = validated_data
        img = KImage.objects.create(**validated_data)
        return img

    def update(self, instance, validated_data):
        # Update the Foo instance
        instance.description = validated_data['description'] 

        if self.initial_data.get('images'):
            validated_data['images'] = self.initial_data['images']
            image_data = validated_data.pop('images')

            for image in image_data:
                c_image= image_data[image]
                instance.image = c_image.name 
        instance.save() 
        return instance
