from rest_framework.parsers import MultiPartParser, FormParser,FileUploadParser, JSONParser
from rest_framework import viewsets

from ..kmodels.sizes_model import SizeModel
from ..kserializers.size_serializers import SizeSerializer
 
class SizesViewSet(viewsets.ModelViewSet):
    queryset = SizeModel.objects.all()
    serializer_class = SizeSerializer

    parser_classes = (JSONParser, FormParser, MultiPartParser, FileUploadParser)