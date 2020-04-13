from django.db import models

from datetime import datetime
from django.utils.timezone import now

from .stitchmodel import Stitch
from .imagemodel import KImage
from .stitchtypemodel import StitchType
from .stitchdesignmodel import StitchTypeDesign
from .timestamp_model import TimestampedModel

class Product(TimestampedModel):
    title= models.CharField(null=True, max_length=80,  default=None) 
    description = models.CharField(null=True, max_length=120,  default=None) 
    images = models.ManyToManyField(KImage, blank=True, default=None)
    
    stitch = models.ForeignKey(Stitch, on_delete=models.CASCADE, default=None, null=True, blank=True)   
    stitch_type = models.ForeignKey(StitchType, on_delete=models.CASCADE, default=None, null=True, blank=True)   
    stitch_type_design = models.ForeignKey(StitchTypeDesign, on_delete=models.CASCADE, default=None, null=True, blank=True)

    user = models.IntegerField(blank=True, null=True) 
    quantity =  models.IntegerField(blank=False, null=False, default=0)

    class Meta:
        db_table = 'knit_product'
        managed = True
        verbose_name = 'Knit Product'
        verbose_name_plural = 'Knit Products'
    
    def __str__(self):
        return self.code

