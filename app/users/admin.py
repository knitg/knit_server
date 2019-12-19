from django.contrib import admin
from django.contrib.auth.models import *
from .kmodels.user_model import User
from .kmodels.customer_model import KCustomer
from .kmodels.image_model import KImage
from .kmodels.address_model import KAddress
from .kmodels.vendor_model import KVendorUser
from .kmodels.usertype_model import KUserType

# Register your models here.
admin.site.unregister(Group)

admin.site.register(KImage)
admin.site.register(KAddress)
admin.site.register(KUserType)
admin.site.register(User)
admin.site.register(KCustomer)
admin.site.register(KVendorUser)