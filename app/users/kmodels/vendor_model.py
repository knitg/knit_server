from django.db import models
from datetime import datetime
from django.conf import settings
from django.utils.timezone import now
from .address_model import KAddress
from .image_model import KImage
from .usertype_model import KUserType
from users.models import User
from .timestamp_model import TimestampedModel
from datetime import datetime, time,date
class KVendorUser(TimestampedModel):
    name= models.CharField(null=True, max_length=80,  default=None)
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=False)

    openTimeStr = "9:30"
    CloseTimeStr = "21:00"
    startTime = datetime.strptime(openTimeStr,"%H:%M")
    endTime = datetime.strptime(CloseTimeStr, "%H:%M")
    
    startTime = startTime.replace(year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)
    endTime = endTime.replace(year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)
    
    openTime = models.TimeField(default=startTime.time(), blank=True, null=True, )
    closeTime = models.TimeField(default=endTime.time(), blank=True, null=True, )

    masters = models.IntegerField(blank=True, null=True, default=None)
    isWeekends = models.BooleanField(default=False, blank=True, null=True)
    alternateDays = models.CharField(max_length=80, blank=True, null=True)
    closed = models.BooleanField(default=False)
    emergency = models.BooleanField(default=False)
    doorService = models.BooleanField(default=False)
    description = models.TextField(max_length=180, blank=True)

    userTypes = models.ManyToManyField(KUserType, blank=True, null=True, default=None)
    images = models.ManyToManyField(KImage, blank=True, null=True, default=None)
    
    class Meta:
        db_table = 'knit_vendor_user'
        managed = True
    
    def __str__(self):
        return self.name
