"""
Django settings for knit_server project.

Generated by 'django-admin startproject' using Django 3.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import datetime
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '8vawxcx622k3=#3sv--80=teohkp-6o&pt48&bt4=+k)i%4(mi'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']
APPEND_SLASH=False

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.auth.hashers',
    'django.contrib.sites',
    'rest_framework',
    

    # ALL AUTHENTICATION MODULE
    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    # REST_AUTH 
    'rest_auth',
    'rest_auth.registration',
    
    # 'allauth.socialaccount.providers.facebook',
    # 'allauth.socialaccount.providers.google',
    # 'allauth.socialaccount.providers.github',
    # 'allauth.socialaccount.providers.linkedin',

    'corsheaders',
    "rest_framework.authtoken", 
    # 'djoser',
    # 'rest_framework_simplejwt',
    # 'social_django',

    'users',
    'products',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # 'social_django.middleware.SocialAuthExceptionMiddleware',
]

ROOT_URLCONF = 'knit_server.urls'
CORS_ORIGIN_ALLOW_ALL = True

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'social_django.context_processors.backends',  # <--
                'social_django.context_processors.login_redirect', # <--
            ],
        },
    },
]

WSGI_APPLICATION = 'knit_server.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'knit_db',
        'USER': 'kuser',
        'PASSWORD':'password',
        'HOST':'139.59.13.86',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET foreign_key_checks = 0;"
        }
    },
    # 'default': {
    #     'ENGINE': 'django.db.backends.mysql',
    #     'NAME': 'knit_db',
    #     'USER': 'knit',
    #     'PASSWORD':'site',
    #     'HOST':'localhost',
    #     'PORT': '3306',
    #     'OPTIONS': {
    #         'init_command': "SET foreign_key_checks = 0;"
    #     }
    # }
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
} 
REST_AUTH_SERIALIZERS = {
    'USER_DETAILS_SERIALIZER': 'users.kserializers.user_serializer.UserSerializer',
    'LOGIN_SERIALIZER': 'users.kserializers.login_serializer.LoginSerializer',
}

REST_SESSION_LOGIN = True
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
SITE_ID = 2
ACCOUNT_EMAIL_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'phone'
ACCOUNT_EMAIL_VERIFICATION = 'optional'

ACCOUNT_EMAIL_REQUIRED = False   
ACCOUNT_USERNAME_REQUIRED = False

# Provider specific settings
SOCIALACCOUNT_PROVIDERS = {
   
}

MEDIA_URL =  '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
]

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
]
AUTH_USER_MODEL = 'users.User'


# DJOSER = {
#     'SERIALIZERS': {
#         'current_user': 'users.kserializers.user_serializer.CurrentUserSerializer',
#         'user_create': 'users.kserializers.user_serializer.UserSerializer',
#         'user': 'users.kserializers.user_serializer.CurrentUserSerializer',        
#     }
# }

SIMPLE_JWT = {
   'AUTH_HEADER_TYPES': ('JWT',),
}

AUTHENTICATION_BACKENDS = [

    "django.contrib.auth.backends.ModelBackend",
    "users.backends.EmailOrPhoneOrUsernameModelBackend",
    "users.backends.EmailAuthenticate", 

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SOCIAL_AUTH_FACEBOOK_KEY = 'your app client id'
SOCIAL_AUTH_FACEBOOK_SECRET = 'your app client secret'
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email', ]  # optional
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {'locale': 'ru_RU'}  # optional


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
# All settings common to all environments 
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'static')
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]