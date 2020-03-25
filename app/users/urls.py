from django.urls import include, path
from rest_framework import routers 
from django.conf.urls import url

from .kviews.address_view import AddressViewSet
from .kviews.usertype_view import UserTypeViewSet
from .kviews.user_view import UserViewSet, UserListViewSet, UserDetailViewSet, UserRegisterViewSet
from .kviews.vendor_view import VendorUserViewSet
from .kviews.image_view import ImageViewSet
from .kviews.login_view import LoginViewSet

router = routers.DefaultRouter(trailing_slash=False)

router.register(r'address', AddressViewSet)
router.register(r'user-types', UserTypeViewSet)
router.register(r'upload', ImageViewSet)
router.register(r'user', UserViewSet) 
router.register(r'users', UserViewSet, basename="usersss") 
router.register(r'vendor', VendorUserViewSet)
user_detail = UserViewSet.as_view({
    'get': 'retrieve'
})
user_list = UserViewSet.as_view({
    'get': 'list'
})
user_update = UserViewSet.as_view({
    'put': 'update',
    'patch': 'update'
})
user_delete = UserViewSet.as_view({
    'delete': 'destroy'
})
login = LoginViewSet.as_view({
    'post': 'create'
})
register = UserViewSet.as_view({
    'post': 'create'
})

# router.register(r'user-detail', user_list, basename='user-detail')

urlpatterns = [ 
    path('', include(router.urls)),
    path('user-detail/<int:pk>', user_detail, name='user-detail'),
    path('user-list', user_list, name='user-list'),
    path('user-update/<int:pk>', user_update, name='user-update'),
    path('user-delete/<int:pk>', user_delete, name='user-delete'),
    path('login', login, name='login'),
	path('register', register, name='register'),
	#path to djoser end points
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
