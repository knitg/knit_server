from rest_framework import serializers
from rest_framework.parsers import JSONParser,MultiPartParser, FormParser,FileUploadParser
from .imageserializer import KImageSerializer
from .category_serializer import CategorySerializer

from ..kmodels.imagemodel import KImage
from ..kmodels.category_model import Category
from ..kmodels.sub_category_model import SubCategory
from ..kmodels.product_model import Product
from ..kmodels.maggam_catalog_model import MaggamCatalog


class MaggamCatalogSerializer(serializers.HyperlinkedModelSerializer):
    # categoryId = serializers.ReadOnlyField(source='category.id')
    # category = serializers.ReadOnlyField(source='category.code')

    images = serializers.SerializerMethodField(read_only=True)
    # category = serializers.SerializerMethodField(read_only=True)
    erros = {}

    def get_images(self, obj):
        serializer = KImageSerializer(obj.images, many=True)
        return serializer.data 

    # def get_category(self, obj):
    #     serializer = CategorySerializer(obj.category, many=True)
    #     return serializer.data 
    
    class Meta:
        model = MaggamCatalog
        fields = ('id','title', 'userId', 'images', 'customizable', 'details')
        parser_classes = (JSONParser, FormParser, MultiPartParser, FileUploadParser) # set parsers if not set in settings. Edited
        
    def validate(self, data):
        data = self.initial_data.get('catalog')
        if data.get('title') is None:
            raise serializers.ValidationError("Maggam catelog title is required")
        if data.get('userId') is None:
            raise serializers.ValidationError("user id is required")
        if self.initial_data.get('catalog_relations') is None:
            if self.initial_data.get('catalog_relations').get("category"):
                raise serializers.ValidationError("Category is required")

        hasMaggamDesign = MaggamCatalog.objects.filter(title= data['title'])
        if len(hasMaggamDesign):
            raise serializers.ValidationError("Maggam Design already existed")
        return data

    def create(self, validated_data):
        ## Image data 
        # validated_data['title'] = validated_data.get('title')
        # validated_data['description'] = self.initial_data.get("description", None)
        try:
            maggam_catalog, created = MaggamCatalog.objects.get_or_create(**validated_data)
            if self.initial_data.get("catalog_relations"):
                files = self.initial_data.get("catalog_relations").get("images")
                if files:
                    
                    for e in maggam_catalog.images.all():
                        maggam_catalog.images.remove(e)
                        KImage.objects.get(id=e.id).delete()

                    for image in files:
                        c_image= files[image]
                        images = KImage.objects.create(image=c_image, description=self.initial_data.get('details'), source='maggam_catalogs/maggam_'+str(maggam_catalog.id), size=c_image.size)
                        maggam_catalog.images.add(images)

            if self.initial_data.get("catalog_relations"):
                category_input = self.initial_data.get("catalog_relations").get("category")
                if category_input:
                    if isinstance(category_input, list):
                        catalog = list(Category.objects.filter(id__in=category_input))
                        maggam_catalog.category.set(catalog)
                    elif isinstance(category_input, str):
                        category_arr = category_input.split(",")
                        catalog = list(Category.objects.filter(id__in=category_arr))
                        maggam_catalog.category.set(catalog)
                    else:
                        logger.warning("NOT SAVED MAGGAM DESIGN : Expected category ids should be an array bug got a {} ".format(self.initial_data.get("category")))
            if created:
                print("Maggam catelog CREATED")
                maggam_catalog.save()

        except MaggamCatalog.DoesNotExist:
            print("MAGGAM CATALOG DOES NOT EXISTS") 

        return maggam_catalog

    def update(self, instance, validated_data):
        # Update the Foo instance
        instance.title = validated_data.get('title', instance.title)
        instance.details = validated_data.get('details', instance.details)
        instance.customizable = validated_data.get('customizable', instance.customizable)
        instance.userId =  validated_data.get('userId', instance.userId).upper()
        instance.save()

        if self.initial_data.get("catalog_relations"):
            files = self.initial_data.get("catalog_relations").get("images")
            if files:
                for e in instance.images.all():
                    instance.images.remove(e)
                    KImage.objects.get(id=e.id).delete()

                for image in files:
                    c_image= files[image]
                    images = KImage.objects.create(image=c_image, description=self.initial_data.get('details'), source='maggam_catalogs/maggam_'+str(instance.id), size=c_image.size)
                    instance.images.add(images) 
            
            if self.initial_data.get("catalog_relations"):
                category_input = self.initial_data.get("catalog_relations").get("category")
                if category_input:
                    if isinstance(category_input, list):
                        catalog = list(Category.objects.filter(id__in=category_input))
                        instance.category.set(catalog)
                    elif isinstance(category_input, str):
                        category_arr = category_input.split(",")
                        catalog = list(Category.objects.filter(id__in=category_arr))
                        instance.category.set(catalog)
                    else:
                        logger.warning("NOT UPDATED MAGGAM DESIGN : Expected category ids should be an array bug got a {} ".format(self.initial_data.get("category")))
            

        return instance
        
            