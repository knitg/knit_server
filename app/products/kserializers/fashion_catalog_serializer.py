from rest_framework import serializers
from rest_framework.parsers import JSONParser,MultiPartParser, FormParser,FileUploadParser
from .imageserializer import KImageSerializer
from .category_serializer import CategorySerializer

from ..kmodels.imagemodel import KImage
from ..kmodels.category_model import Category
from ..kmodels.sub_category_model import SubCategory
from ..kmodels.product_model import Product
from ..kmodels.fashion_catalog_model import FashionCatalog


class FashionCatalogSerializer(serializers.HyperlinkedModelSerializer):
    images = serializers.SerializerMethodField(read_only=True)
    category = serializers.SerializerMethodField(read_only=True)
    erros = {}

    def get_images(self, obj):
        serializer = KImageSerializer(obj.images, many=True)
        return serializer.data 

    def get_category(self, obj):
        serializer = CategorySerializer(obj.category, many=True)
        return serializer.data 
    
    class Meta:
        model = FashionCatalog
        fields = ('id','title', 'userId', 'images', 'category','customizable', 'details')
        parser_classes = (JSONParser, FormParser, MultiPartParser, FileUploadParser) # set parsers if not set in settings. Edited
        
    def validate(self, data):
        if data.get('title') is None:
            raise serializers.ValidationError("Fashion catelog title is required")
        if data.get('userId') is None:
            raise serializers.ValidationError("user id is required")
        if data.get('category') is None:
            raise serializers.ValidationError("Category is required")

        hasFashionDesign = FashionCatalog.objects.filter(code= data['code'])
        if len(hasFashionDesign):
            raise serializers.ValidationError("Fashion Design already existed")
        return data

    def create(self, validated_data):
        ## Image data 
        # validated_data['title'] = validated_data.get('title')
        # validated_data['description'] = self.initial_data.get("description", None)
        try:
            fashion_catalog, created = FashionCatalog.objects.get_or_create(**validated_data)
            if self.initial_data.get("images"):
                for e in fashion_catalog.images.all():
                    fashion_catalog.images.remove(e)
                    KImage.objects.get(id=e.id).delete()
            if self.initial_data.get("category"):
                if isinstance(self.initial_data.get("category"), list):
                    catalog = list(MaggamCatalog.objects.filter(id__in=self.initial_data.get("category")))
                    fashion_catalog.category.set(catalog)
                else:
                    logger.warning("NOT SAVED FASHION DESIGN : Expected color ids should be an array bug got a {} ".format(self.initial_data.get("category")))
            if created:
                print("Fashion catelog CREATED")
                fashion_catalog.save()

        except FashionCatalog.DoesNotExist:
            print("MAGGAM CATALOG DOES NOT EXISTS")
        
        if self.initial_data.get('images'):
            image_data = self.initial_data.get('images')
            for image in image_data:
                c_image= image_data[image]
                images = KImage.objects.create(image=c_image, description=self.initial_data.get('details'), source='maggam_catalog_'+str(maggam_catalog.id), size=c_image.size)
                category.images.add(images)         

        return maggam_catalog

    def update(self, instance, validated_data):
        try:
            maggam_catalog, created = FashionCatalog.objects.update_or_create(**validated_data)
            if created:
                print("Fashion catelog update")
                maggam_catalog.save()
            if self.initial_data.get("images"):
                for e in maggam_catalog.images.all():
                    maggam_catalog.images.remove(e)
                    KImage.objects.get(id=e.id).delete()
            maggam_catalog.save()
        except FashionCatalog.DoesNotExist:
            print("MAGGAM CATALOG DOES NOT EXISTS")
        
        if self.initial_data.get('images'):
            image_data = self.initial_data.get('images')
            for image in image_data:
                c_image= image_data[image]
                images = KImage.objects.create(image=c_image, description=self.initial_data.get('details'), source='maggam_catalog_'+str(maggam_catalog.id), size=c_image.size)
                category.images.add(images)         

        # Update the Foo instance
        # instance.title = validated_data.get('title', instance.title)
        # instance.description = validated_data.get('description', instance.description)
        # instance.code =  validated_data.get('code', instance.code).upper()   
        # instance.save()

        # if self.initial_data.get('images'):
        #     validated_data['images'] = self.initial_data['images']
        #     image_data = validated_data.pop('images')

        #     ### Remove relational images if any ####
        #     for e in instance.images.all():
        #         instance.images.remove(e)
        #         KImage.objects.get(id=e.id).delete()
        #     for image in image_data:
        #         c_image= image_data[image]
        #         images = KImage.objects.create(image=c_image, description=self.initial_data.get('description'), source='category_'+str(instance.id), size=c_image.size)
        #         instance.images.add(images)

        # return instance
    
            