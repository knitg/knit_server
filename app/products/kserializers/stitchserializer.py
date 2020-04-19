from rest_framework import serializers
from rest_framework.parsers import JSONParser,MultiPartParser, FormParser,FileUploadParser
from .imageserializer import KImageSerializer

from ..kmodels.imagemodel import KImage
from ..kmodels.stitchmodel import Stitch
from ..kmodels.stitchtypemodel import StitchType
from ..kmodels.stitchdesignmodel import StitchTypeDesign
from ..kmodels.product_model import Product


class StitchSerializer(serializers.HyperlinkedModelSerializer):
    images = serializers.SerializerMethodField(read_only=True)

    def get_images(self, obj):
        serializer = KImageSerializer(obj.images, many=True)
        return serializer.data 
    
    class Meta:
        model = Stitch
        fields = ('id','type', 'code', 'images')
        parser_classes = (JSONParser, FormParser, MultiPartParser, FileUploadParser) # set parsers if not set in settings. Edited
        
    def validate(self, data):
        if data.get('type'):
            data['code'] = data.get('type', '').replace(" ", "_").upper()
        else:
            raise serializers.ValidationError("Stitch type is required")
        return data

    def create(self, validated_data):
        ## Image data 
        validated_data['code'] = validated_data.get('code')
        stitch = Stitch.objects.create(**validated_data)
        stitch.save()

        if self.initial_data.get('images'):
            image_data = self.initial_data.get('images')
            for image in image_data:
                c_image= image_data[image]
                images = KImage.objects.create(image=c_image, description=self.initial_data.get('description'), source='stitch_'+str(stitch.id), size=c_image.size)
                stitch.images.add(images)         

        return stitch

    def update(self, instance, validated_data):
        # Update the Foo instance
        instance.type = validated_data.get('type', instance.type)
        instance.description = validated_data.get('description', instance.description)
        instance.code =  validated_data.get('code', instance.code).upper()   
        instance.save()

        if self.initial_data.get('images'):
            validated_data['images'] = self.initial_data['images']
            image_data = validated_data.pop('images')

            ### Remove relational images if any ####
            for e in instance.images.all():
                instance.images.remove(e)
                KImage.objects.get(id=e.id).delete()
            for image in image_data:
                c_image= image_data[image]
                images = KImage.objects.create(image=c_image, description=self.initial_data.get('description'), source='stitch_'+str(instance.id), size=c_image.size)
                instance.images.add(images)

        return instance
    
            