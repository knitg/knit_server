from rest_framework import serializers
from ..kmodels.address_model import KAddress

class KAddressSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = KAddress
        fields = "__all__"

