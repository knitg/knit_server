from django.db import models
from .timestamp_model import TimestampedModel

class UserType(TimestampedModel):
    user_type= models.CharField(null=True, max_length=80,  default=None)  
    description = models.CharField(max_length=150, blank=True, null=True)
    class Meta:
        db_table = 'ref_user_types'
    
    def __repr__(self):
        return super().__repr__() + "User type: " + str(self.user_type) 

    def __str__(self):
        return "{}, {}".format(self.user_type, self.description)
