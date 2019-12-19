from django.db import models

from datetime import datetime
from django.utils.timezone import now

from .stitchmodel import Stitch
from .imagemodel import KImage
from .stitchtypemodel import StitchType

class StitchTypeDesign(models.Model):
    sdesign= models.CharField(null=True, max_length=80,  default=None) 
    stitch_type = models.ForeignKey(StitchType, on_delete=models.CASCADE, default=None, blank=True, null=True)
    images = models.ManyToManyField(KImage, blank=True, null=True, default=None)
    code = models.CharField(null=True, max_length=80,  default=None) 
    description = models.CharField(null=True, max_length=120,  default=None) 
    created_at = models.DateTimeField(default=now, editable=False)
    updated_at = models.DateTimeField(default=now, editable=False)

    class Meta:
        db_table = 'knit_stitch_type_design'
        managed = True
        verbose_name = 'Knit Stitch Type design'
        verbose_name_plural = 'Knit Stitch Type design'
    
    def __str__(self):
        return self.sdesign