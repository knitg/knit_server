from django.db import models

from datetime import datetime
from django.utils.timezone import now

from .stitchmodel import Stitch
from .imagemodel import KImage
from .stitchtypemodel import StitchType
from .timestamp_model import TimestampedModel 
from .color_model import ColorModel
from .sizes_model import SizeModel
from .offers_model import Offers

class Product(TimestampedModel):

    # Product basic info
    title= models.CharField(null=True, max_length=80,  default=None) 
    description = models.CharField(null=True, max_length=120,  default=None) 
    quantity =  models.IntegerField(blank=False, null=False, default=0)
    in_stock =  models.BooleanField(default=True, blank=True, null=True)
    price = models.FloatField(blank=False, null=False, default=0.00)

    # Product details
    images = models.ManyToManyField(KImage, blank=True, default=None)
    offers = models.ManyToManyField(Offers, blank=True, default=None)
    colors = models.ManyToManyField(ColorModel, blank=True, default=None)
    sizes = models.ManyToManyField(SizeModel, blank=True, default=None)
    
    #Categorys
    stitch = models.ManyToManyField(Stitch)
    stitch_type = models.ManyToManyField(StitchType)

    #Product belongs to vendor
    user = models.IntegerField(blank=True, null=True) 

    class Meta:
        db_table = 'knit_product'
        managed = True
        verbose_name = 'Knit Product'
        verbose_name_plural = 'Knit Products'
    
    def __str__(self):
        return self.code

