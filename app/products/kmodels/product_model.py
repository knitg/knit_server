from django.db import models

from datetime import datetime
from django.utils.timezone import now

from .category_model import Category
from .imagemodel import KImage
from .sub_category_model import SubCategory
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
    category = models.ManyToManyField(Category)
    sub_Category = models.ManyToManyField(SubCategory)

    #Product belongs to vendor
    user = models.IntegerField(blank=True, null=True) 

    class Meta:
        db_table = 'product'
        managed = True
    
    def __str__(self):
        return self.code

