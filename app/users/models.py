from django.db import models
from datetime import datetime
from django.utils.timezone import now
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings
from model_utils import Choices
 
from .kmodels.image_model import KImage
from .kmodels.address_model import KAddress
from .kmodels.usertype_model import KUserType


"""
    # USER MANAGER ACTIONS HERE
"""

class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username, phone, user_type=1, user_role='GUEST', email=None, password=None, images=None):
        if not phone:
            raise ValueError('Users must have an Phone number')
        if not username:
            username = phone
        user = self.model(
            username = username,
            phone = phone,
            email = email,
            user_role= user_role
        )
        user.set_password(password)
        
        user.is_admin =False
        user.is_active =True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username=None, phone=None, user_type='CUSTOMER', user_role='GUEST', email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        user = self.create_user(username, phone, email=email, password=password)
        user.is_admin = True 
        user.save(using=self._db)
        return user

#### USER MODEL

class User(AbstractBaseUser):
    USER_ROLE = Choices(
        ('USER', 'USER'),
        ('ADMIN', 'ADMIN'),
        ('LEADER', 'LEADER'),
        ('SUPER_ADMIN', 'SUPER ADMIN'),
        ('GUEST', 'GUEST'),
        ('DEL_BOY', 'DELIVERY BOY'),
    )
    username = models.CharField("User Name", max_length=50, unique=True)
    images = models.ManyToManyField(KImage, blank=True, null=True, default=None)
    phone = models.CharField("Phone Number", max_length=50, unique=True)
    email = models.EmailField("Email Address", blank=True, null= True)
    password = models.CharField('password', max_length=128, null=False)
    user_type = models.ManyToManyField(KUserType, blank=True, null=True, default=None)
    user_role = models.CharField(max_length=80, choices=USER_ROLE, default=USER_ROLE.GUEST)
    
    is_admin = models.IntegerField(default=False, blank=True, null=True)
    is_staff = models.IntegerField(default=False, blank=True, null=True)
    is_active = models.IntegerField(default=False, blank=True, null=True)
    is_superuser = models.IntegerField(blank=True, null=True, default=False)

    objects = UserManager()

    @property
    def is_superuser(self):
        return self.is_admin

    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['user_type', 'user_role']

    class Meta:
        db_table = 'user'
        managed = True
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return self.phone

    def __unicode__(self):
        return 
