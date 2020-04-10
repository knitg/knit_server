from rest_framework import serializers
from ..kmodels.address_model import KAddress

class KAddressSerializer(serializers.ModelSerializer):
    full_address = serializers.ReadOnlyField(source="get_full_address", required=False)
    class Meta:
        model = KAddress
        fields = ("id", "address_line_1", "address_line_2", "postalCode", "full_address")
        # fields = "__all__"
