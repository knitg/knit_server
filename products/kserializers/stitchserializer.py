from rest_framework import serializers
from rest_framework.parsers import MultiPartParser, FormParser,FileUploadParser
from .imageserializer import KImageSerializer

from ..kmodels.imagemodel import KImage
from ..kmodels.stitchmodel import Stitch
from ..kmodels.stitchtypemodel import StitchType
from ..kmodels.stitchdesignmodel import StitchTypeDesign
from ..kmodels.productmodel import Product


class StitchSerializer(serializers.HyperlinkedModelSerializer):
    images = KImageSerializer(many=True, required=False, allow_null=True)
    class Meta:
        model = Stitch
        fields = ('id','stype', 'code', 'description', 'images')
        parser_classes = (FormParser, MultiPartParser, FileUploadParser) # set parsers if not set in settings. Edited

    def create(self, validated_data):
        ## Image data 
        validated_data['code'] = validated_data['code'].upper() if validated_data['code'] else None
        stitch = Stitch.objects.create(**validated_data)
        stitch.save()

        if self.initial_data.get('images'):
            validated_data['images'] = self.initial_data['images']
            image_data = validated_data.pop('images')
            for image in image_data:
                c_image= image_data[image]
                images = KImage.objects.create(image=c_image, description=self.initial_data.get('description'), source='stitch_'+str(stitch.id), size=c_image.size)
                stitch.images.add(images)         

        return stitch

    def update(self, instance, validated_data):
        # Update the Foo instance
        instance.stype = validated_data['stype']
        instance.description = validated_data['description']
        instance.code =  validated_data['code'].upper() if validated_data['code'] else instance.code   
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
    
            