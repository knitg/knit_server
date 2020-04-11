from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import *
from users.models import User
from .kmodels.image_model import KImage
from .kmodels.address_model import Address
from .kmodels.vendor_model import Vendor
from .kmodels.usertype_model import UserType

from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin  as BaseUserAdmin
class UserAdmin(UserAdmin):

    list_display = ('username', 'email','phone', 'is_admin')
    list_filter = ('is_admin',)

    fieldsets = (
        (None, {'fields': ('username', 'email','phone','password')}),

        ('Permissions', {'fields': ('is_admin',)}),
    )

    search_fields =  ('username', 'email','phone')
    ordering = ('username','email','phone')

    filter_horizontal = ()


# Register your models here.
admin.site.unregister(Group)

admin.site.register(KImage)
admin.site.register(Address)
admin.site.register(UserType)
admin.site.register(User, UserAdmin)
admin.site.register(Vendor)