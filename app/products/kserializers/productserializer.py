from rest_framework import serializers

from ..kmodels.imagemodel import KImage
from ..kmodels.stitchmodel import Stitch
from ..kmodels.stitchtypemodel import StitchType
from ..kmodels.stitchdesignmodel import StitchTypeDesign
from ..kmodels.product_model import Product
from ..kmodels.color_model import ColorModel
from ..kmodels.sizes_model import SizeModel


from rest_framework.parsers import MultiPartParser, FormParser,FileUploadParser
from .imageserializer import KImageSerializer
from .stitchserializer import StitchSerializer
from .stitchtypeserializer import StitchTypeSerializer
from .stitchdesignserializer import StitchTypeDesignSerializer
from .price_serializer import PriceSerializer
from .stitchdesignserializer import StitchTypeDesignSerializer
from .color_choices_serializers import ColorChoiceSerilizer
from .size_choices_serializers import SizeChoiceSerilizer
from .offers_serializer import OfferSerializer


import re

import logging
logger = logging.getLogger(__name__)

class ProductSerializer(serializers.ModelSerializer):

    stitch = serializers.SerializerMethodField(read_only=True)
    stitch_type = serializers.SerializerMethodField(read_only=True)
    stitch_type_design = serializers.SerializerMethodField(read_only=True)
    colors = serializers.SerializerMethodField(read_only=True)
    sizes = serializers.SerializerMethodField(read_only=True)
    offers = serializers.SerializerMethodField(read_only=True)
    images = serializers.SerializerMethodField(read_only=True)
    errors = {}


    def get_stitch(self,obj):
        serializer = StitchSerializer(obj.stitch, many=True)
        return serializer.data 

    def get_stitch_type(self,obj):
        serializer = StitchTypeSerializer(obj.stitch_type, many=True)
        return serializer.data 

    def get_stitch_type_design(self,obj):
        serializer = StitchTypeDesignSerializer(obj.stitch_type_design, many=True)
        return serializer.data 

    def get_offers(self,obj):
        serializer = OfferSerializer(obj.offers, many=True)
        return serializer.data 

    def get_colors(self,obj):
        serializer = ColorChoiceSerilizer(obj.colors, many=True)
        return serializer.data 

    def get_sizes(self,obj):
        serializer = SizeChoiceSerilizer(obj.sizes, many=True)
        return serializer.data 

    def get_images(self, obj):
        serializer = KImageSerializer(obj.images, many=True)
        return serializer.data 

        
    class Meta:
        model = Product
        fields = ('id', 'title','description', 'quantity', 'colors', 'sizes', 'offers', 'stitch', 'stitch_type', 'stitch_type_design', 'images')

    def validate(self, data):
        self.errors = {}
        data = self.initial_data.get('product')
        if data.get('title') is None:
            logger.error("Product title is required")
            raise serializers.ValidationError("Product title is required")
        if data.get('quantity', 0) != 0:
            data['quantity'] = data.get('quantity', None)
        else:
            logger.error("Product Quantity is required")
            self.errors['quanity_required'] = "Product Quantity is required"
        if data.get('price'):
            data['price'] = data.get('price', None)
        else:
            logger.error("Product Price is required")
            self.errors['price_required'] = "Product Price is required"
        logger.error(self.errors)
        raise serializers.ValidationError(self.errors)
        return data

    def create(self, validated_data):
        #Handling many to many fields
        validated_data = self.initial_data.get("product")
        images = validated_data.pop("images") if validated_data.get('images') else None
        offers = validated_data.pop("offers") if validated_data.get('offers') else None
        colors = validated_data.pop("colors") if validated_data.get('colors') else None
        sizes = validated_data.pop("sizes") if validated_data.get('sizes') else None
        stitch = validated_data.pop("stitch") if validated_data.get('stitch') else None
        stitch_type = validated_data.pop("stitch_type") if validated_data.get('stitch_type') else None
        stitch_type_design = validated_data.pop("stitch_type_design") if validated_data.get('stitch_type_design') else None

        product = Product.objects.create(**validated_data)
        
        # COLORS RELATION HERE
        if colors:
            if isinstance(colors, list):
                color = list(ColorModel.objects.filter(id__in=colors))
                product.colors.set(color)
            else:
                logger.warning("NOT SAVED COLORS : Expected color ids should be an array bug got a {} ".format(type(colors)))
        
        # SIZES RELATION HERE
        if sizes:
            if isinstance(sizes, list):
                size = list(SizeModel.objects.filter(size__contains=sizes))
                product.sizes.set(size)
            else:
                logger.warning("NOT SAVED SIZES : Expected color ids should be an array bug got a {} ".format(type(sizes)))
        
        # OFFERS RELATION HERE
        if offers:
            if isinstance(sizes, list):
                size = list(SizeModel.objects.filter(id__in=sizes))
                product.sizes.set(size)
            else:
                logger.warning("NOT SAVED SIZES : Expected color ids should be an array bug got a {} ".format(type(sizes)))
        
        # STITCH CATEGORY RELATION HERE
        if stitch:
            if isinstance(stitch, list):
                stitch1 = list(Stitch.objects.filter(id__in=stitch))
                product.stitch.set(stitch1)
            else:
                logger.warning("NOT SAVED IN STITCH CATEGORY : Expected stitch ids should be an array bug got a {} ".format(type(stitch)))
        
        # STITCH TYPE CATEGORY RELATION HERE
        if stitch_type:
            if isinstance(stitch_type, list):
                stitch_type_1 = list(ColorModel.objects.filter(id__in=stitch_type))
                product.colors.set(stitch_type_1)
            else:
                logger.warning("NOT SAVED STITCH TYPE CATEGORY : Expected stitch_type ids should be an array bug got a {} ".format(type(stitch_type)))
        
        # STITCH TYPE DESIGN CATEGORY RELATION HERE
        if stitch_type_design:
            if isinstance(stitch_type_design, list):
                stitch_type_design1 = list(ColorModel.objects.filter(id__in=stitch_type_design))
                product.colors.set(stitch_type_design1)
            else:
                logger.warning("NOT SAVED STITCH TYPE DESIGN CATEGORY  : Expected STITCH TYPE DESIGN ids should be an array bug got a {} ".format(type(colors)))
        
        # IMAGES RELATION HERE
        if images: 
            for image in images:
                c_image= image_data[image]
                images = KImage.objects.create(image=c_image, description=self.initial_data.get('description'), source='user_'+str(user.id), size=c_image.size)
                instance.images.add(images)
        

        product.save() 
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
