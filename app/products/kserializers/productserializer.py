from rest_framework import serializers

from ..kmodels.imagemodel import KImage
from ..kmodels.stitchmodel import Stitch
from ..kmodels.stitchtypemodel import StitchType
from ..kmodels.stitchdesignmodel import StitchTypeDesign
from ..kmodels.productmodel import Product

from rest_framework.parsers import MultiPartParser, FormParser,FileUploadParser
from .imageserializer import KImageSerializer
from .stitchserializer import StitchSerializer
from .stitchtypeserializer import StitchTypeSerializer
from .stitchdesignserializer import StitchTypeDesignSerializer

import re

class ProductSerializer(serializers.HyperlinkedModelSerializer):
    stitch = StitchSerializer(many=False, required=False)
    stitch_type = StitchTypeSerializer(many=False, required=False)
    images = KImageSerializer(many=True, required=False, allow_null=False)
    # stitch = StitchSerializer(many=False)
    class Meta:
        model = Product
        # exclude = ['code']
        # fields = ('id','code', 'title','description', 'stitch','stitch_type','stitch_type_design','user', 'images')
        fields = '__all__'
    
    def create(self, validated_data):
        if not (self.initial_data.get('title', None) is None):
            validated_data['code'] = re.sub('[\s+]', '', self.initial_data.get('title'))
        ## Image data
        if not (self.initial_data.get('stitch', None) is None):
            stitchQuerySet = Stitch.objects.filter(id= self.initial_data.get('stitch', 0))
            stitch = serializers.PrimaryKeyRelatedField(queryset=stitchQuerySet, many=False)
            if len(stitchQuerySet):
                validated_data['stitch'] = stitchQuerySet[0]
        if not (self.initial_data.get('stitch_type', None) is None):
            stitchTypeQuerySet = StitchType.objects.filter(id= self.initial_data.get('stitch_type', 0))
            stitch_type = serializers.PrimaryKeyRelatedField(queryset=stitchTypeQuerySet, many=False)
            if len(stitchTypeQuerySet):
                validated_data['stitch_type'] = stitchTypeQuerySet[0]
        
        if not (self.initial_data.get('stitch_type_design', None) is None):
            stitchTypeDesignQuerySet = StitchType.objects.filter(id= self.initial_data.get('stitch_type_design', 0))
            stitch_type_design = serializers.PrimaryKeyRelatedField(queryset=stitchTypeDesignQuerySet, many=False)
            if len(stitchTypeDesignQuerySet):
                validated_data['stitch_type_design'] = stitchTypeDesignQuerySet[0]

        
        product = Product.objects.create(**validated_data)
        product.save()

        if self.initial_data.get('images'):
            validated_data['images'] = self.initial_data['images']
            image_data = validated_data.pop('images')
            for image in image_data:
                c_image= image_data[image]
                images = KImage.objects.create(image=c_image, description=self.initial_data.get('description'), source='product_'+str(product.id), size=c_image.size)
                product.images.add(images)         

        return product

    def update(self, instance, validated_data):
        # Update the Foo instance
        instance.title = self.initial_data['title'] if self.initial_data.get('title') else instance.title
        instance.description = self.initial_data['description'] if self.initial_data.get('description') else instance.description
        instance.quantity = self.initial_data['quantity'] if self.initial_data.get('quantity') else instance.quantity
        instance.stitched_date = self.initial_data['stitched_date'] if self.initial_data.get('stitched_date') else instance.stitched_date
        
        if not (self.initial_data.get('stitch', None) is None):
            stitchQuerySet = Stitch.objects.filter(id= self.initial_data.get('stitch', 0))
            stitch = serializers.PrimaryKeyRelatedField(queryset=stitchQuerySet, many=False)
            if len(stitchQuerySet):
                validated_data['stitch'] = stitchQuerySet[0]
        if not (self.initial_data.get('stitch_type', None) is None):
            stitchTypeQuerySet = StitchType.objects.filter(id= self.initial_data.get('stitch_type', 0))
            stitch_type = serializers.PrimaryKeyRelatedField(queryset=stitchTypeQuerySet, many=False)
            if len(stitchTypeQuerySet):
                validated_data['stitch_type'] = stitchTypeQuerySet[0]
        
        if not (self.initial_data.get('stitch_type_design', None) is None):
            stitchTypeDesignQuerySet = StitchType.objects.filter(id= self.initial_data.get('stitch_type_design', 0))
            stitch_type_design = serializers.PrimaryKeyRelatedField(queryset=stitchTypeDesignQuerySet, many=False)
            if len(stitchTypeDesignQuerySet):
                validated_data['stitch_type_design'] = stitchTypeDesignQuerySet[0]

        if not (self.initial_data.get('title', None) is None):
            instance.code = re.sub('[\s+]', '', self.initial_data.get('title'))
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
                images = KImage.objects.create(image=c_image, description=self.initial_data.get('description'), source='product_'+str(instance.id), size=c_image.size)
                instance.images.add(images)

        return instance

###
#   Product Serializer returns products with foreignkey hyperlinks
###

class ProductLinkSerializer(serializers.HyperlinkedModelSerializer):
    
    images = KImageSerializer(many=True, required=False, allow_null=False)
    class Meta:
        model = Product
        fields = ('id','code', 'title','description', 'stitch','stitch_type','stitch_type_design','user', 'images')
