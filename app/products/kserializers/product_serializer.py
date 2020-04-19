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
from .stitchdesignserializer import StitchTypeDesignSerializer
from .color_serializers import ColorSerilizer
from .size_serializers import SizeSerializer
from .offers_serializer import OfferSerializer

import re

import logging
logger = logging.getLogger(__name__)

class ProductListSerializer(serializers.ModelSerializer):  
    class Meta:
        model = Product
        fields = ('id', 'title','description', 'quantity', 'price')


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
        serializer = ColorSerilizer(obj.colors, many=True)
        return serializer.data 

    def get_sizes(self,obj):
        serializer = SizeSerializer(obj.sizes, many=True)
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
        if self.instance is None:
            if data.get('title') is None:
                logger.error("Product title is required")
                raise serializers.ValidationError("Product title is required")
            if self.instance is None and data.get('quantity', 0) != 0:
                data['quantity'] = data.get('quantity', None)
            else:
                logger.error("Product Quantity is required")
                self.errors['quanity_required'] = "Product Quantity is required"
            if self.instance is None and data.get('price'):
                data['price'] = data.get('price', None)
            else:
                logger.error("Product Price is required")
                self.errors['price_required'] = "Product Price is required"
            if self.instance is None and data.get('user'):
                data['user'] = data.get('user', None)
            else:
                logger.error("Product User is required")
                self.errors['user_required'] = "Product user is required"
            logger.error(self.errors)
            raise serializers.ValidationError(self.errors)
        return data

    def create(self, validated_data):
        #Handling many to many fields
        validated_data = self.initial_data.get("product")
        product_relations = self.initial_data.get("product_relations")
        
        product = Product.objects.create(**validated_data) 
        self.setProductRelations(product, product_relations)
        
        product.save() 
        return product

    def update(self, instance, validated_data):
        product_input = self.initial_data.get("product")
        product_relations = self.initial_data.get("product_relations")
        
        instance.title = product_input.get('title', instance.title)
        instance.description = product_input.get('description', instance.description)
        instance.quantity = product_input.get('quantity', instance.quantity)
        instance.price = product_input.get('price', instance.price)
        instance.user = product_input.get('user', instance.user)
        instance.in_stock = product_input.get('in_stock', instance.in_stock)

        self.setProductRelations(instance, product_relations)
        instance.save() 
        return instance

    def setProductRelations(self, product, product_relations):
        # COLORS RELATION HERE
        if product:
            if product_relations.get('colors'):
                if isinstance(product_relations.get('colors'), list):
                    color = list(ColorModel.objects.filter(id__in=product_relations.get('colors')))
                    product.colors.set(color)
                else:
                    logger.warning("NOT SAVED COLORS : Expected color ids should be an array bug got a {} ".format(type(colors)))
            
            # SIZES RELATION HERE
            if product_relations.get('sizes'):
                if isinstance(product_relations.get('sizes'), list):
                    size = list(SizeModel.objects.filter(id__in=product_relations.get('sizes')))
                    product.sizes.set(size)
                else:
                    logger.warning("NOT SAVED SIZES : Expected color ids should be an array bug got a {} ".format(type(sizes)))
            
            # OFFERS RELATION HERE
            if product_relations.get('offers'):
                if isinstance(product_relations.get('offers'), list):
                    size = list(SizeModel.objects.filter(id__in=product_relations.get('offers')))
                    product.sizes.set(size)
                else:
                    logger.warning("NOT SAVED SIZES : Expected color ids should be an array bug got a {} ".format(type(sizes)))
            
            # IMAGES RELATION HERE
            if product_relations.get('images'):
                for e in product_relations.get('images').images.all():
                    instance.images.remove(e)
                    KImage.objects.get(id=e.id).delete()
                for image in product_relations.get('images'):
                    c_image= image_data[image]
                    images = KImage.objects.create(image=c_image, description=self.initial_data.get('description'), source='user_'+str(user.id), size=c_image.size)
                    product.images.add(images)

            # STITCH CATEGORY RELATION HERE
            if product_relations.get('stitch'):
                if isinstance(product_relations.get('stitch'), list):
                    stitch1 = list(Stitch.objects.filter(id__in=product_relations.get('stitch')))
                    product.stitch.set(stitch1)
                else:
                    logger.warning("NOT SAVED IN STITCH CATEGORY : Expected stitch ids should be an array bug got a {} ".format(type(stitch)))
            
            # STITCH TYPE CATEGORY RELATION HERE
            if product_relations.get('stitch_type'):
                if isinstance(product_relations.get('stitch_type'), list):
                    stitch_type_1 = list(ColorModel.objects.filter(id__in=product_relations.get('stitch_type')))
                    product.colors.set(stitch_type_1)
                else:
                    logger.warning("NOT SAVED STITCH TYPE CATEGORY : Expected stitch_type ids should be an array bug got a {} ".format(type(stitch_type)))
            
            # STITCH TYPE DESIGN CATEGORY RELATION HERE
            if product_relations.get('stitch_type_design'):
                if isinstance(product_relations.get('stitch_type_design'), list):
                    stitch_type_design1 = list(ColorModel.objects.filter(id__in=product_relations.get('stitch_type_design')))
                    product.colors.set(stitch_type_design1)
                else:
                    logger.warning("NOT SAVED STITCH TYPE DESIGN CATEGORY  : Expected STITCH TYPE DESIGN ids should be an array bug got a {} ".format(type(colors)))
        
 