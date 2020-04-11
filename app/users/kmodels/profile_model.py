from django.db import models
from .timestamp_model import TimestampedModel

from .image_model import KImage
from .address_model import Address
from .usertype_model import UserType
from .vendor_model import Vendor

class Profile(TimestampedModel):
    user = models.OneToOneField(
        'users.User', on_delete=models.CASCADE
    )
    # Personal details 
    firstName = models.TextField(blank=True, null=True, default='')
    lastName = models.TextField(blank=True, null=True, default='')
    gender = models.IntegerField(blank=True, default=None, null=True)
    married = models.BooleanField(default=False)
    birthday = models.DateTimeField(blank=True, default=None, null=True)
    anniversary = models.DateTimeField(blank=True, default=None, null=True)
    
    userTypes = models.ManyToManyField(UserType)
    user_role = models.CharField(max_length=80, blank=True, null=True, default=None)
    images = models.ManyToManyField(KImage)
    address = models.ManyToManyField(Address)

    # In addition to the `bio` field, each user may have a profile image or
    # avatar. This field is not required and it may be blank.
    image = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)

    def get_full_name(self):
        return "%s %s" % (self.firstName, self.lastName)
 

    def get_default_image(self):
        return 'https://static.productionready.io/images/smiley-cyrus.jpg'

    def __str__(self):
        return "%s %s" % (self.firstName, self.lastName)