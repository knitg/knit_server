from django.db import models

from datetime import datetime
from django.utils.timezone import now

from .stitchmodel import Stitch
from .imagemodel import KImage
from .stitchtypemodel import StitchType
from .stitchdesignmodel import StitchTypeDesign

class Product(models.Model):
    code = models.CharField(null=True, max_length=80,  default=None) 
    title= models.CharField(null=True, max_length=80,  default=None) 
    description = models.CharField(null=True, max_length=120,  default=None) 
    images = models.ManyToManyField(KImage, blank=True, null=True, default=None)
    stitch = models.ForeignKey(Stitch, on_delete=models.CASCADE, default=None, null=True, blank=True)   
    stitch_type = models.ForeignKey(StitchType, on_delete=models.CASCADE, default=None, null=True, blank=True)   
    stitch_type_design = models.ForeignKey(StitchTypeDesign, on_delete=models.CASCADE, default=None, null=True, blank=True)
    user =  models.CharField(max_length=20,  default=None, blank=False, null=False)
    created_at = models.DateTimeField(default=now, editable=False)
    updated_at = models.DateTimeField(default=now, editable=False)

    class Meta:
        db_table = 'knit_product'
        managed = True
        verbose_name = 'Knit Product'
        verbose_name_plural = 'Knit Products'
    
    def __str__(self):
        return self.code

