from rest_framework import serializers
from rest_framework.parsers import JSONParser,MultiPartParser, FormParser,FileUploadParser
from .imageserializer import KImageSerializer

from ..kmodels.imagemodel import KImage
from ..kmodels.category_model import Category
from ..kmodels.sub_category_model import SubCategory
from ..kmodels.product_model import Product


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    images = serializers.SerializerMethodField(read_only=True)
    erros = {}
    def get_images(self, obj):
        serializer = KImageSerializer(obj.images, many=True)
        return serializer.data 
    
    class Meta:
        model = Category
        fields = ('id','title', 'code', 'images', 'description')
        parser_classes = (JSONParser, FormParser, MultiPartParser, FileUploadParser) # set parsers if not set in settings. Edited
        
    def validate(self, data):
        if data.get('title'):
            data['code'] = data.get('title', '').replace(" ", "_").upper()            
        else:
            raise serializers.ValidationError("Category title is required")
        return data

    def create(self, validated_data):
        ## Image data 
        validated_data['code'] = validated_data.get('code')
        validated_data['description'] = self.initial_data.get("description", None)
        try:
            category = Category.objects.get(code=validated_data.get("code"))
            category.title = validated_data.get('title', category.title)
            category.description = validated_data.get('description', category.description)
            category.code =  validated_data.get('code', category.code).upper()
            if self.initial_data.get("images"):
                for e in category.images.all():
                    category.images.remove(e)
                    KImage.objects.get(id=e.id).delete()
            category.save()
        except Category.DoesNotExist:
            category = Category(**validated_data)
            category.save()
        
        if self.initial_data.get('images'):
            image_data = self.initial_data.get('images')
            for image in image_data:
                c_image= image_data[image]
                images = KImage.objects.create(image=c_image, description=self.initial_data.get('description'), source='category_'+str(category.id), size=c_image.size)
                category.images.add(images)         

        return category

    def update(self, instance, validated_data):
        # Update the Foo instance
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.code =  validated_data.get('code', instance.code).upper()   
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
                images = KImage.objects.create(image=c_image, description=self.initial_data.get('description'), source='category_'+str(instance.id), size=c_image.size)
                instance.images.add(images)

        return instance
    
            