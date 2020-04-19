from rest_framework import serializers
from rest_framework.parsers import JSONParser,MultiPartParser, FormParser,FileUploadParser

from ..kmodels.product_order_model import ProductOrder
import arrow

import logging
logger = logging.getLogger(__name__)

class ProductOrderSerializer(serializers.ModelSerializer):
    errors = {}

    class Meta:
        model = ProductOrder
        fields = ('id','product_id', 'details')
        parser_classes = (JSONParser, FormParser, MultiPartParser, FileUploadParser) # set parsers if not set in settings. Edited


    def validate(self, data):
        self.errors = {}
        data = self.initial_data.get('data')
        if data.get('product_id') is None:
            self.errors['required'] = 'Product id is required'        
  
        raise serializers.ValidationError(self.errors)        
        return data

    def create(self, validated_data):
        ## Image data
        validated_data = self.initial_data.get('data')
        product_order = ProductOrder.objects.create(**validated_data)
        product_order.save()
        return product_order

    def update(self, instance, validated_data):
        # Update the Foo instance
        validated_data = self.initial_data.get('data')
        instance.product_id = validated_data.get('product_id', instance.product_id)
        instance.details = validated_data.get('details', instance.details)
        instance.save()
        return instance 