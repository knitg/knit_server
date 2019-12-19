from rest_framework import serializers
from rest_framework.parsers import MultiPartParser, FormParser,FileUploadParser

from .imageserializer import KImageSerializer
from .stitchserializer import StitchSerializer
from .stitchtypeserializer import StitchTypeSerializer

from ..kmodels.imagemodel import KImage
from ..kmodels.stitchmodel import Stitch
from ..kmodels.stitchtypemodel import StitchType
from ..kmodels.stitchdesignmodel import StitchTypeDesign
from ..kmodels.productmodel import Product

class StitchTypeDesignSerializer(serializers.HyperlinkedModelSerializer):
    stitch_type = StitchTypeSerializer(many=False, required=False)
    images = KImageSerializer(many=True, required=False, allow_null=True) 
    class Meta:
        model = StitchTypeDesign
        fields = ('id', 'sdesign', 'code', 'description', 'stitch_type', 'images')
    
    def create(self, validated_data):
        ## Image data
        validated_data['code'] = validated_data['code'].upper() if validated_data['code'] else None
        if self.initial_data['stitch_type']:
            stitchTypeQuerySet = StitchType.objects.filter(id= self.initial_data['stitch_type'])
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
                images = KImage.objects.create(image=c_image, description=self.initial_data.get('description'), source='stitch_design_'+str(product.id), size=c_image.size)
                stitchdesign.images.add(images)         

        return stitchdesign

    def update(self, instance, validated_data):
        # Update the Foo instance
        instance.sdesign = validated_data['sdesign']
        instance.description = validated_data['description']
        instance.code = validated_data['code'].upper() if validated_data['code'] else instance.code

        if self.initial_data['stitch_type']:
            stitchTypeQuerySet = StitchType.objects.filter(id= self.initial_data['stitch_type'])
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
