from django.urls import include, path
from rest_framework import routers 
from django.conf.urls import url

from .kviews.address_view import AddressViewSet
from .kviews.usertype_view import UserTypeViewSet
from .kviews.user_view import UserViewSet
from .kviews.customer_view import CustomerViewSet
from .kviews.vendor_view import VendorUserViewSet
from .kviews.image_view import ImageViewSet
from .kviews.login_view import LoginViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'address', AddressViewSet)
router.register(r'user-types', UserTypeViewSet)
router.register(r'upload', ImageViewSet)
router.register(r'user', UserViewSet)
router.register(r'login', LoginViewSet)
router.register(r'customer', CustomerViewSet)
router.register(r'vendor', VendorUserViewSet)

urlpatterns = [ 
    path('', include(router.urls)),
]
