from rest_framework import serializers
from rest_framework.parsers import JSONParser,MultiPartParser, FormParser,FileUploadParser

from ..kmodels.offers_model import Offers
import arrow

import logging
logger = logging.getLogger(__name__)
class OfferSerializer(serializers.ModelSerializer):
    errors = {}

    class Meta:
        model = Offers
        fields = ('id','title','code','discount', 'from_date','to_date', 'is_active')
        parser_classes = (JSONParser, FormParser, MultiPartParser, FileUploadParser) # set parsers if not set in settings. Edited


    def validate(self, data):
        self.errors = {}
        data = self.initial_data.get("data")
        if data.get('code'):
            data['code'] = data.get('code', '').replace(" ", "_").upper()
        else:
            self.errors['required'] = 'code field is required'
        if data.get('title') is None:
            self.errors['required'] = 'title field is required'

        if data.get('from_date') is None:
            self.errors['required'] = 'from_date field is required'
        else:
            data['from_date'] = arrow.get(data.get('from_date')).format('YYYY-MM-DD HH:mm:ss')
            logger.info("from date - {}".format(data['from_date']))

        if data.get('to_date') is None:
            self.errors['required'] = 'to_date field is required'
        else:
            data['to_date'] = arrow.get(data.get('to_date')).format('YYYY-MM-DD HH:mm:ss')
            logger.info("to date - {}".format(data['to_date']))

        raise serializers.ValidationError(self.errors)        
        return data

    def create(self, validated_data):
        ## Image data
        validated_data = self.initial_data.get('data')
        offer = Offers.objects.create(**validated_data)
        offer.save()
        return offer

    def update(self, instance, validated_data):
        # Update the Foo instance
        validated_data = self.initial_data.get('data')
        instance.title = validated_data.get('title', instance.title)
        instance.code = validated_data.get('code', instance.code).upper()
        instance.discount = validated_data.get('discount', instance.discount)
        instance.from_date = validated_data.get('from_date', instance.from_date)
        instance.to_date = validated_data.get('to_date', instance.to_date)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()

        return instance 