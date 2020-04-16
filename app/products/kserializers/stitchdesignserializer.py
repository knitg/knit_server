from rest_framework import serializers

from .imageserializer import KImageSerializer
from .stitchserializer import StitchSerializer
from .stitchtypeserializer import StitchTypeSerializer

from ..kmodels.imagemodel import KImage
from ..kmodels.stitchmodel import Stitch
from ..kmodels.stitchtypemodel import StitchType
from ..kmodels.stitchdesignmodel import StitchTypeDesign
from ..kmodels.product_model import Product

import logging
logger = logging.getLogger(__name__)

class StitchTypeDesignSerializer(serializers.HyperlinkedModelSerializer):
    images = serializers.SerializerMethodField(read_only=True, allow_null=True)
    stitchTypeId = serializers.ReadOnlyField(source='stitch_type.id')
    stitchType = serializers.ReadOnlyField(source='stitch_type.type')
    errors = {}
    def get_images(self, obj):
        serializer = KImageSerializer(obj.images, many=True)
        return serializer.data
    
    class Meta:
        model = StitchTypeDesign
        fields = ('id', 'type', 'code', 'description', 'stitchTypeId', 'stitchType', 'images')
    
    def validate(self, data):
        self.errors = {}
        if self.initial_data.get('stitch_type') is None:
            self.errors['stitch_type'] = 'Stitch Type is required'
        if self.initial_data.get('type'):
            data['code'] = self.initial_data.get('type', '').replace(" ", "_").upper()
        else:
            self.errors['required'] = 'Stitch design type is required'
        if len(self.errors):
            logger.info(self.errors)
            raise serializers.ValidationError(self.errors)
        return data

    def create(self, validated_data):
        ## Image data
        validated_data['code'] = validated_data['code'].upper() if validated_data['code'] else None
        if self.initial_data['stitch_type']:
            stitchTypeQuerySet = StitchType.objects.filter(id= int(self.initial_data['stitch_type']))
            stitch_type = serializers.PrimaryKeyRelatedField(queryset=stitchTypeQuerySet, many=False)
            if len(stitchTypeQuerySet):
                validated_data['stitch_type'] = stitchTypeQuerySet[0]

        stitchdesign = StitchTypeDesign.objects.create(**validated_data)
        stitchdesign.save()

        if self.initial_data.get('images'):
            validated_data['images'] = self.initial_data['images']
            image_data = validated_data.pop('images')
            for image in image_data:
                c_image= image_data[image]
                images = KImage.objects.create(image=c_image, description=self.initial_data.get('description'), source='stitch_design_'+str(stitchdesign.id), size=c_image.size)
                stitchdesign.images.add(images)         

        return stitchdesign

    def update(self, instance, validated_data):
        # Update the Foo instance
        instance.type = validated_data.get('type', instance.type)
        instance.description = validated_data.get('description', instance.description)
        instance.code =  validated_data.get('code', instance.code).upper()   
        
        if self.initial_data['stitch_type']:
            stitchTypeQuerySet = StitchType.objects.filter(id= int(self.initial_data['stitch_type']))
            instance.stitch_type = stitchTypeQuerySet[0] if len(stitchTypeQuerySet) else None

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
                images = KImage.objects.create(image=c_image, description=self.initial_data.get('description'), source='stitch_design_'+str(instance.id), size=c_image.size)
                instance.images.add(images)

        return instance
