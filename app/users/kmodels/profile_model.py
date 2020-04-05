from django.db import models
from .timestamp_model import TimestampedModel

from .image_model import KImage
from .address_model import KAddress
from .usertype_model import KUserType

class Profile(TimestampedModel):
    user = models.OneToOneField(
        'users.User', on_delete=models.CASCADE
    )
    # Personal details 
    firstName = models.TextField(blank=True)
    lastName = models.TextField(blank=True)
    gender = models.IntegerField(blank=True, default=None, null=True)
    married = models.BooleanField(default=False)
    birthday = models.DateTimeField(blank=True, default=None, null=True)
    anniversary = models.DateTimeField(blank=True, default=None, null=True)
    
    userTypes = models.ManyToManyField(KUserType, blank=True, null=True, default=None)
    user_role = models.CharField(max_length=80, blank=True, null=True, default=None)
    images = models.ManyToManyField(KImage, blank=True, null=True, default=None)
    address = models.ManyToManyField(KAddress, blank=True, null=True, default=None)

    # In addition to the `bio` field, each user may have a profile image or
    # avatar. This field is not required and it may be blank.
    image = models.URLField(blank=True)

    def get_full_name(self):
        return "%s %s" % (self.firstName, self.lastName)

    def __str__(self):
        return self.user.username