from django.urls import include, path
from rest_framework import routers 
from django.conf.urls import url

from .kviews.address_view import AddressViewSet
from .kviews.usertype_view import UserTypeViewSet
from .kviews.user_view import UserViewSet, UserListViewSet, UserDetailViewSet, UserRegisterViewSet
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
# router.register(r'user', UserViewSet) 
router.register(r'profiles', ProfileListViewSet)
router.register(r'users', UserViewSet, basename="usersss") 
router.register(r'vendor', VendorUserViewSet)

urlpatterns = [ 
    path('', include(router.urls)),
    path('user/<int:user_id>/profile', ProfileViewSet.as_view({'get': 'list','put': 'update'}), name='profile'),
    # url(r'^rest-auth/facebook/$', FacebookConnectView.as_view(), name='fb_login'),
    # url(r'^rest-auth/twitter/$', TwitterConnectView.as_view(), name='twitter_login'),
    # url(r'^rest-auth/github/$', GithubConnectView.as_view(), name='github_login'),
    # url(r'^socialaccounts/$', SocialAccountListView.as_view(), name='social_account_list'),
    # url(r'^socialaccounts/(?P<pk>\d+)/disconnect/$', SocialAccountDisconnectView.as_view(), name='social_account_disconnect'),
	
]
