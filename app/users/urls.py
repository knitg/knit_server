from django.urls import include, path
from rest_framework import routers 
from django.conf.urls import url

from .kviews.address_view import AddressViewSet
from .kviews.usertype_view import UserTypeViewSet
from .kviews.user_view import UserViewSet, UserListViewSet
from .kviews.customer_view import CustomerViewSet
from .kviews.vendor_view import VendorUserViewSet
from .kviews.image_view import ImageViewSet
from .kviews.login_view import LoginViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'address', AddressViewSet)
router.register(r'user-types', UserTypeViewSet)
router.register(r'upload', ImageViewSet)
router.register(r'login', UserViewSet)
router.register(r'user-list', UserListViewSet, basename='user-list')
router.register(r'customer', CustomerViewSet)
router.register(r'vendor', VendorUserViewSet)

urlpatterns = [ 
    path('', include(router.urls)),
	#path to djoser end points
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
