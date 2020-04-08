from rest_framework import serializers
from ..kmodels.address_model import KAddress

class KAddressSerializer(serializers.ModelSerializer):
    full_address = serializers.CharField(source="get_full_address")
    class Meta:
        model = KAddress
        fields = "__all__"

