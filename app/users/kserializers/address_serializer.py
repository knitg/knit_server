from rest_framework import serializers
from ..kmodels.address_model import KAddress

class KAddressSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = KAddress
        fields = ['id', 'address_line_1', 'address_line_2', 'url', 
        'landmark', 'postalCode', 'latitude', 'longitude',
        'geoAddress', 'city', 'state', 'created_at', 'updated_at'
        ]

