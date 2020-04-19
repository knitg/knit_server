from rest_framework import serializers
from rest_framework.parsers import JSONParser,MultiPartParser, FormParser,FileUploadParser

from ..kmodels.stitch_order_model import StitchOrder
import arrow

import logging
logger = logging.getLogger(__name__)

class StitchOrderSerializer(serializers.ModelSerializer):
    errors = {}

    class Meta:
        model = StitchOrder
        fields = ('id','title', 'details', 'expected_date', 'emergency', 'stitch_id', 'is_vfm', 'material_types')
        parser_classes = (JSONParser, FormParser, MultiPartParser, FileUploadParser) # set parsers if not set in settings. Edited


    def validate(self, data):
        self.errors = {}
        data = self.initial_data.get('data')
        if data.get('title') is None:
            self.errors['required'] = 'Title is required'
        if data.get('stitch_id') is None:
            self.errors['required'] = 'stitch_id field is required'
        
  
        raise serializers.ValidationError(self.errors)        
        return data

    def create(self, validated_data):
        ## Image data
        validated_data = self.initial_data.get('data')
        stitch_order = StitchOrder.objects.create(**validated_data)
        stitch_order.save()
        return stitch_order

    def update(self, instance, validated_data):
        # Update the Foo instance
        validated_data = self.initial_data.get('data')
        instance.title = validated_data.get('title', instance.title)
        instance.details = validated_data.get('details', instance.details)
        instance.expected_date = validated_data.get('expected_date', instance.expected_date)
        instance.emergency = validated_data.get('emergency', instance.emergency)
        instance.stitch_id = validated_data.get('stitch_id', instance.stitch_id)
        instance.is_vfm = validated_data.get('is_vfm', instance.is_vfm)
        instance.material_types = validated_data.get('material_types', instance.material_types)
        instance.save()

        return instance 