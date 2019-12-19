from rest_framework import serializers
from rest_framework.parsers import MultiPartParser, FormParser,FileUploadParser
from .imageserializer import KImageSerializer
from .stitchserializer import StitchSerializer

from ..kmodels.imagemodel import KImage
from ..kmodels.stitchmodel import Stitch
from ..kmodels.stitchtypemodel import StitchType
from ..kmodels.stitchdesignmodel import StitchTypeDesign
from ..kmodels.productmodel import Product


class StitchTypeSerializer(serializers.ModelSerializer):
    stitch = StitchSerializer(many=False, required=False)
    images = KImageSerializer(many=True, required=False, allow_null=True)

    class Meta:
        model = StitchType
        fields = ('id', 'stype', 'code', 'description', 'stitch', 'images')

    def create(self, validated_data):
        ## Image data
        validated_data['code'] = validated_data['code'].upper() if validated_data['code'] else None
        if self.initial_data['stitch']:
            stitchQuerySet = Stitch.objects.filter(id= self.initial_data['stitch'])
            stitch = serializers.PrimaryKeyRelatedField(queryset=stitchQuerySet, many=False)
            if len(stitchQuerySet):
                validated_data['stitch'] = stitchQuerySet[0]

        stitchtype = StitchType.objects.create(**validated_data)
        stitchtype.save()

        if self.initial_data.get('images'):
            validated_data['images'] = self.initial_data['images']
            image_data = validated_data.pop('images')
            for image in image_data:
                c_image= image_data[image]
                images = KImage.objects.create(image=c_image, description=self.initial_data.get('description'), source='stitchtype_'+str(stitchtype.id), size=c_image.size)
                stitchtype.images.add(images)         

        return stitchtype

    def update(self, instance, validated_data):
        # Update the Foo instance
        instance.stype = validated_data['stype']
        instance.description = validated_data['description']
        instance.code =  validated_data['code'].upper() if validated_data['code'] else instance.code   
        
        if self.initial_data['stitch']:
            stitchQuerySet = Stitch.objects.filter(id= self.initial_data['stitch'])
            instance.stitch = stitchQuerySet[0] if len(stitchQuerySet) else None        
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
                images = KImage.objects.create(image=c_image, description=self.initial_data.get('description'), source='stitchtype_'+str(instance.id), size=c_image.size)
                instance.images.add(images)

        return instance

class StitchTypeByStitchSerializer(serializers.HyperlinkedModelSerializer):
    # stitch = StitchSerializer(many=False, required=False)
    images = KImageSerializer(many=True, required=False, allow_null=False)
    # stitch = StitchSerializer(many=False)
    class Meta:
        model = StitchType
        fields = ('stype', 'code', 'description', 'images')