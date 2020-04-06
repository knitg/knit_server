from django.urls import include, path
from rest_framework import routers 
from django.conf.urls import url

from .kviews.address_view import AddressViewSet
from .kviews.usertype_view import UserTypeViewSet
from .kviews.user_view import UserViewSet, UserFilterViewSet
from .kviews.vendor_view import VendorUserViewSet
from .kviews.image_view import ImageViewSet
from .kviews.login_view import LoginViewSet
from .kviews.profile_view import ProfileListViewSet, ProfileViewSet
from .kviews.sociallogin_view import FacebookConnectView, TwitterConnectView, GithubConnectView
from rest_auth.registration.views import (SocialAccountListView, SocialAccountDisconnectView)

router = routers.DefaultRouter(trailing_slash=False)

router.register(r'address', AddressViewSet)
router.register(r'user-types', UserTypeViewSet)
router.register(r'upload', ImageViewSet)
router.register(r'users', UserViewSet) 
router.register(r'userfilter', UserFilterViewSet) 
router.register(r'profiles', ProfileListViewSet)
router.register(r'vendor', VendorUserViewSet)

urlpatterns = [ 
    path('', include(router.urls)),
    path('user/<int:user_id>/profile', ProfileViewSet.as_view({'get': 'list','put': 'update'}), name='profile'),
    
]

# ---- # ----- # ---- HOW TO USE FILTER END POINTS ---- # --------- # -----------#

    # http://localhost:8000/user/userfilter?id__in=2,4,5
    # http://localhost:8000/user/userfilter?username__contains=Mahi&email=mahi6535@gmail.com
    # http://localhost:8000/user/userfilter?email__icontians=mahi6535@gmail.com

#-------------Related models profile-----------------#

    # http://localhost:8000/user/userfilter?profile__userTypes__in=2
    # http://localhost:8000/user/userfilter?profile__firstName__icontains=Mahi