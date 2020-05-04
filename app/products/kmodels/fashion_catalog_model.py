from django.db import models
from .imagemodel import KImage
from .category_model import Category

from datetime import datetime
from django.utils.timezone import now
from .timestamp_model import TimestampedModel

# order type is what type of order user will make?
class FashionCatalog(models.Model):
    title = models.CharField(null=True, max_length=80,  default=None)
    userId = models.IntegerField(null=True, default=None)
    category = models.ManyToManyField(Category ,null=True, default=None)
    images = models.ManyToManyField(KImage, blank=True, default=None)
    customizable = models.BooleanField(blank=True, null=True, default=False)
    details = models.CharField(null=True, max_length=80,  default=None)

    class Meta:
        db_table = 'fashion_catalog'
        managed = True
    
    def __str__(self):
        return self.title

    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


