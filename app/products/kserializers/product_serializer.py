from rest_framework import serializers

from ..kmodels.imagemodel import KImage
from ..kmodels.category_model import Category
from ..kmodels.sub_category_model import SubCategory
from ..kmodels.product_model import Product
from ..kmodels.color_model import ColorModel
from ..kmodels.sizes_model import SizeModel


from rest_framework.parsers import MultiPartParser, FormParser,FileUploadParser
from .imageserializer import KImageSerializer
from .category_serializer import CategorySerializer
from .sub_category_serializer import SubCategorySerializer
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

    category = serializers.SerializerMethodField(read_only=True)
    sub_category = serializers.SerializerMethodField(read_only=True)
    colors = serializers.SerializerMethodField(read_only=True)
    sizes = serializers.SerializerMethodField(read_only=True)
    offers = serializers.SerializerMethodField(read_only=True)
    images = serializers.SerializerMethodField(read_only=True)
    errors = {}


    def get_category(self,obj):
        serializer = CategorySerializer(obj.category, many=True)
        return serializer.data 

    def get_sub_category(self,obj):
        serializer = SubCategorySerializer(obj.sub_category, many=True)
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
        fields = ('id', 'title','description', 'quantity', 'colors', 'sizes', 'offers', 'category', 'sub_category', 'images')

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

            # CATEGORY RELATION HERE
            if product_relations.get('category'):
                if isinstance(product_relations.get('category'), list):
                    category_list = list(Stitch.objects.filter(id__in=product_relations.get('category')))
                    product.category.set(category_list)
                else:
                    logger.warning("NOT SAVED IN CATEGORY CATEGORY : Expected category ids should be an array bug got a {} ".format(type(category)))
            
            # SUB CATEGORYRELATION HERE
            if product_relations.get('sub_category'):
                if isinstance(product_relations.get('sub_category'), list):
                    sub_category = list(ColorModel.objects.filter(id__in=product_relations.get('sub_category')))
                    product.colors.set(sub_category)
                else:
                    logger.warning("NOT SAVED SUB CATEGORY TYPE CATEGORY : Expected sub_category ids should be an array bug got a {} ".format(type(sub_category)))
            