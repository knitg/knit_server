from django.db import models
from datetime import datetime
from django.utils.timezone import now
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings
from model_utils import Choices
 
from .kmodels.timestamp_model import TimestampedModel

"""
    # USER MANAGER ACTIONS HERE
"""

class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username, phone, email=None, password=None, **extra_fields):
        # if not phone and not Email:
        #     raise ValueError('Users must have an Phone number')
        # if not username:
        #     username = phone
        # if not email:
        #     email = phone
        user = self.model(
            username = username,
            phone = phone,
            email = email
        )
        user.set_password(password)
        
        user.is_admin =False
        user.is_active =True
        user.save(using=self._db)
        return user

    def create_superuser(self, username=None, phone=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        user = self.create_user(username, phone, email=email, password=password)
        user.is_admin = True 
        user.save(using=self._db)
        return user

#### USER MODEL

class User(AbstractBaseUser, TimestampedModel):
    username = models.CharField(db_index=True, max_length=255, blank=True, null=True)
    phone = models.CharField(db_index=True, max_length=50, blank=True, null=True, unique=True)
    email = models.EmailField(db_index=True, blank=True, null=True)
    password = models.CharField('password', max_length=128, null=False)
    
    is_admin = models.IntegerField(default=False, blank=True, null=True)
    is_staff = models.IntegerField(default=False, blank=True, null=True)
    is_active = models.BooleanField(default=True)
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
    REQUIRED_FIELDS = ['email','username']

    class Meta:
        db_table = 'user'
        managed = True
        verbose_name = 'user'
        verbose_name_plural = 'users'
        ordering = ['-created_at', '-updated_at']

    def __str__(self):
        return self.phone

    def __unicode__(self):
        return 
