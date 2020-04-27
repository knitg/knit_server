import os
import csv
from django.conf import settings
from django.core.files import File

from django.shortcuts import render 
from rest_framework.parsers import MultiPartParser, FormParser,FileUploadParser, JSONParser
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from ..kmodels.stitchmodel import Stitch
from ..kmodels.stitchtypemodel import StitchType
from ..kserializers.stitchserializer import StitchSerializer
from ..kserializers.stitchtypeserializer import StitchTypeSerializer

import logging
logger = logging.getLogger(__name__)
from django.db.models import Q
## USER CAN UPLOAD STITCH FROM CSV/EXCEL
class CSVUploadStitchViewSet(viewsets.ModelViewSet):
    queryset = Stitch.objects.all()
    serializer_class = StitchSerializer
     
    parser_classes = (JSONParser, FormParser, MultiPartParser, FileUploadParser) # set parsers if not set in settings. Edited

    def create(self, request, *args, **kwargs):
        logger.info(" \n\n ----- CSV STITCH CREATE initiated -----")
        results = []
        for csv_file in request.FILES:
            logger.info(" \n\n ----- CSV VENDOR CREATE initiated -----")
            decoded_file = request.FILES[csv_file].read().decode('utf-8').splitlines()
            csv_reader = csv.DictReader(decoded_file)
            for i, row in enumerate(csv_reader):
                if row:
                    logger.info(" \n\n")
                    logger.info(row)
                    stitch_data = {}
                    stitch_data['type'] = row.get('type')                    
                    desc = row.get('description').encode('ascii','ignore')
                    stitch_data['description'] = desc.decode("utf-8")[:100]
                    if row.get("image"):
                        with open(row.get('image'), 'rb') as f:
                            stitch_data['images'] = {'images' : File(f) }
                            logger.info(stitch_data['images'])
                    
                    logger.info("PREPARED STITCH DATA ", stitch_data)                    
                    stitch_serializer = StitchSerializer(data= stitch_data)
                    logger.info(stitch_serializer.is_valid())       
                    stitch_serializer.is_valid(raise_exception=True)
                    try:
                        logger.info("Before serializer save call")
                        stitch_serializer.save()
                        logger.info({'stitchId':stitch_serializer.instance.id, 'status':'200 Ok'})
                        print("SAVED Stitch")
                        results.append({'stitchId':stitch_serializer.instance.id, "status":status.HTTP_201_CREATED})
                    except Exception:
                        logger.error("Something wrong with stitch serializer save")
                        print("Already has the Stitch")
        return Response(results, status=status.HTTP_201_CREATED)


## USER CAN UPLOAD STITCH TYPES FROM CSV/EXCEL
class CSVUploadStitchTypeViewSet(viewsets.ModelViewSet):
    queryset = StitchType.objects.all()
    serializer_class = StitchTypeSerializer
     
    parser_classes = (JSONParser, FormParser, MultiPartParser, FileUploadParser) # set parsers if not set in settings. Edited

    def create(self, request, *args, **kwargs):
        logger.info(" \n\n ----- CSV STITCH TYPE CREATE initiated -----")
        results = []
        for csv_file in request.FILES:
            decoded_file = request.FILES[csv_file].read().decode(errors='replace').splitlines()
            csv_reader = csv.DictReader(decoded_file)
            for i, row in enumerate(csv_reader):
                if row:
                    logger.info(" \n\n")
                    logger.info(row)
                    print(row)
                    stitch_data = {}
                    stitch_data['type'] = row.get('type')
                    stitch_obj = Stitch.objects.filter(code__icontains=row.get("stitch-code"))
                    logger.info("---- STITCH OBJ --- ")
                    logger.info(stitch_obj)
                    if len(stitch_obj):
                        stitch_data['stitch'] = stitch_obj[0].id
                    desc = row.get('description').encode('ascii','ignore')
                    stitch_data['description'] = desc.decode("utf-8")[:200]
                    if row.get("image"):
                        with open(row.get('image'), 'rb') as f:
                            stitch_data['images'] = {'images' : File(f) }
                            logger.info(stitch_data['images'])

                    logger.info("PREPARED STITCH DATA ", stitch_data)                    
                    stitchtype_serializer = StitchTypeSerializer(data= stitch_data)
                    logger.info(stitchtype_serializer.is_valid())
                    stitchtype_serializer.is_valid(raise_exception=True)
                    try:
                        logger.info("Before serializer save call")
                        stitchtype_serializer.save()
                        logger.info({'stitchTypeId':stitchtype_serializer.instance.id, 'status':'200 Ok'})
                        print("SAVED Stitch Type")
                        results.append({'stitchTypeId':stitchtype_serializer.instance.id, "status":status.HTTP_201_CREATED})
                    except Exception:
                        logger.error("Something wrong with stitch type serializer save")
                        print("Already has the Stitch Type")
        return Response(results, status=status.HTTP_201_CREATED)