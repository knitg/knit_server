from rest_framework import serializers
from ..kmodels.sizes_model import SizeModel

class SizeChoiceSerilizer(serializers.ModelSerializer):
    class Meta:
        model = SizeModel
        fields = ('id', 'size')
