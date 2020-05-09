from django.db import models
from datetime import datetime
from django.conf import settings
from django.utils.timezone import now
from .address_model import Address
from .usertype_model import UserType
from .image_model import KImage 
from users.models import User
from .timestamp_model import TimestampedModel

import os
import csv


class Vendor(models.Model):
    name= models.CharField(null=True, max_length=80,  default=None)
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    openTime = models.TimeField(blank=True, null=True )
    closeTime = models.TimeField(blank=True, null=True )

    masters = models.IntegerField(blank=True, null=True, default=None)
    isWeekends = models.BooleanField(default=False, blank=True, null=True)
    alternateDays = models.CharField(max_length=80, blank=True, null=True)
    closed = models.BooleanField(default=False, blank=True, null=True)
    emergency = models.BooleanField(default=False, blank=True, null=True)
    doorService = models.BooleanField(default=False, blank=True, null=True)
    description = models.TextField(max_length=180, blank=True, null=True)
    
    images = models.ManyToManyField(KImage, blank=True, default=None)
    address = models.ManyToManyField(Address, blank=True, default=None)
    userTypes = models.ManyToManyField(UserType, blank=True, default=None)
    
    class Meta:
        db_table = 'knit_vendor'
        managed = True
    
    def __str__(self):
        return self.name

