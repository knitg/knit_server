from django.db import models

from .stitchmodel import Stitch
from .imagemodel import KImage

from datetime import datetime
from django.utils.timezone import now

class StitchType(models.Model):
    stype= models.CharField(null=True, max_length=80,  default=None) 
    stitch = models.ForeignKey(Stitch, on_delete=models.CASCADE, blank=False, null=False, default=None)
    images = models.ManyToManyField(KImage, blank=True, null=True, default=None)
    code = models.CharField(null=True, max_length=80,  default=None) 
    description = models.CharField(null=True, max_length=120,  default=None) 
    created_at = models.DateTimeField(default=now, editable=False)
    updated_at = models.DateTimeField(default=now, editable=False)

    class Meta:
        db_table = 'knit_stitch_type'
        managed = True
        verbose_name = 'Knit Stitch Type Ref Table'
        verbose_name_plural = 'Knit Stitch Type Ref Table'
    
    def __str__(self):
        return self.stype 