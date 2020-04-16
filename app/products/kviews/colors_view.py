from rest_framework.parsers import MultiPartParser, FormParser,FileUploadParser, JSONParser
from rest_framework import viewsets

from ..kmodels.color_model import ColorModel
from ..kserializers.color_choices_serializers import ColorChoiceSerilizer
 

class ColorsViewSet(viewsets.ModelViewSet):
    queryset = ColorModel.objects.all()
    serializer_class = ColorChoiceSerilizer

    parser_classes = (JSONParser, FormParser, MultiPartParser, FileUploadParser)