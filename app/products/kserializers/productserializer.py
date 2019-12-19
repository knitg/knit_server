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

class ProductSerializer(serializers.HyperlinkedModelSerializer):
    stitch = StitchSerializer(many=False, required=False)
    stitch_type = StitchTypeSerializer(many=False, required=False)
    images = KImageSerializer(many=True, required=False, allow_null=False)
    # stitch = StitchSerializer(many=False)
    class Meta:
        model = Product
        fields = ('id','code', 'title','description', 'stitch','stitch_type','stitch_type_design','user', 'images')
    
    def create(self, validated_data):
        ## Image data
        if self.initial_data['stitch']:
            if self.initial_data['stitch']:
                stitchQuerySet = Stitch.objects.filter(id= self.initial_data['stitch'])
                stitch = serializers.PrimaryKeyRelatedField(queryset=stitchQuerySet, many=False)
            if self.initial_data['stitch_type']:
                stitchTypeQuerySet = StitchType.objects.filter(id= self.initial_data['stitch_type'])
                stitch_type = serializers.PrimaryKeyRelatedField(queryset=stitchTypeQuerySet, many=False)
            if len(stitchQuerySet):
                validated_data['stitch'] = stitchQuerySet[0]
            if len(stitchTypeQuerySet):
                validated_data['stitch_type'] = stitchTypeQuerySet[0]

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
        instance.title = validated_data['title']
        instance.description = validated_data['description']
        instance.code = validated_data['code']

        if self.initial_data['stitch']:
            stitchQuerySet = Stitch.objects.filter(id= self.initial_data['stitch'])
            instance.stitch = stitchQuerySet[0] if len(stitchQuerySet) else None
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
