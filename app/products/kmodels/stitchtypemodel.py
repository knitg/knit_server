from django.db import models

from .stitchmodel import Stitch
from .imagemodel import KImage
from .timestamp_model import TimestampedModel
from datetime import datetime
from django.utils.timezone import now

class StitchType(TimestampedModel):
    type = models.CharField(null=True, max_length=80,  default=None) 
    stitch = models.ForeignKey(Stitch, on_delete=models.CASCADE, blank=False, null=False, default=None)
    images = models.ManyToManyField(KImage, blank=True, default=None)
    code = models.CharField(null=True, max_length=80,  default=None) 
    description = models.CharField(null=True, max_length=250,  default=None) 
    
    class Meta:
        db_table = 'knit_stitch_type'
        managed = True
        verbose_name = 'Knit Stitch Type Ref Table'
        verbose_name_plural = 'Knit Stitch Type Ref Table'
    
    def __str__(self):
        return self.type 