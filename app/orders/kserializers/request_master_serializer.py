from rest_framework import serializers
from rest_framework.parsers import JSONParser,MultiPartParser, FormParser,FileUploadParser

from ..kmodels.request_masters_model import RequestMaster
import arrow

import logging
logger = logging.getLogger(__name__)

class RequestMasterSerializer(serializers.ModelSerializer):
    errors = {}

    class Meta:
        model = RequestMaster
        fields = ('id','duration', 'details', 'from_date', 'to_date', 'master_id', 'is_vfm')
        parser_classes = (JSONParser, FormParser, MultiPartParser, FileUploadParser) # set parsers if not set in settings. Edited


    def validate(self, data):
        self.errors = {}
        data = self.initial_data.get("data")
        if data.get('duration') is None:
            self.errors['required'] = 'Duration field is required'
  
        raise serializers.ValidationError(self.errors)        
        return data

    def create(self, validated_data):
        ## Image data
        validated_data = self.initial_data.get('data')
        order_master = RequestMaster.objects.create(**validated_data)
        order_master.save()
        return order_master

    def update(self, instance, validated_data):
        # Update the Foo instance
        validated_data = self.initial_data.get('data')
        instance.duration = validated_data.get('duration', instance.duration)
        instance.details = validated_data.get('details', instance.details)
        instance.from_date = validated_data.get('from_date', instance.from_date)
        instance.to_date = validated_data.get('to_date', instance.to_date)
        instance.master_id = validated_data.get('master_id', instance.master_id)
        instance.is_vfm = validated_data.get('is_vfm', instance.is_vfm)
        instance.save()

        return instance 