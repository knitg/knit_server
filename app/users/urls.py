from django.urls import include, path
from rest_framework import routers 
from django.conf.urls import url

from .kviews.address_view import AddressViewSet
from .kviews.usertype_view import UserTypeViewSet
from .kviews.user_view import UserViewSet
from .kviews.vendor_view import VendorUserViewSet, UploadVendorSpreadSheetViewSet
from .kviews.image_view import ImageViewSet
from .kviews.login_view import LoginViewSet
from .kviews.profile_view import ProfileListViewSet, ProfileViewSet
from .kviews.sociallogin_view import FacebookConnectView, TwitterConnectView, GithubConnectView
from rest_auth.registration.views import (SocialAccountListView, SocialAccountDisconnectView)

from .kviews.csv_user_ref_tables_view import CSVUploadUserRefTblViewSet


router = routers.DefaultRouter(trailing_slash=False)

router.register(r'address', AddressViewSet)
router.register(r'user-types', UserTypeViewSet)
router.register(r'upload', ImageViewSet)
router.register(r'users', UserViewSet)
router.register(r'profiles', ProfileListViewSet, )
router.register(r'vendors', VendorUserViewSet, basename="vendors")
router.register(r'csv-vendors', UploadVendorSpreadSheetViewSet, basename="csv_vendors")
router.register(r'csv-user-ref-tables', CSVUploadUserRefTblViewSet, basename="csv-user-ref-tables")

urlpatterns = [ 
    path('', include(router.urls)),
    path('<int:user_id>/profile', ProfileViewSet.as_view({'get': 'list','put': 'update'}), name='profile'),
    
]

# --------=============== HOW TO USE SEARCH USER END POINTS (native search) ===================---------#

    # http://localhost:8000/user/user?search=94410 (phonenumber search)
    # http://localhost:8000/user/userfilter?search=mahi6535@gm (email search)
    # http://localhost:8000/user/userfilter?search=mbg (username search)

#------================= Related models profile ==========================-------#
    # http://localhost:8000/user/users?profile__userTypes__in=2
    # http://localhost:8000/user/userfilter?profile__userTypes__in=2
    # http://localhost:8000/user/userfilter?profile__firstName__icontains=Mahi

# -------================ Filter and search with PAGINATION ====================--------------#

    # http://localhost:8000/user/users?page=2&phone__contains=94    
    # http://localhost:8000/user/users?page=1&username__icontains=mah   
    # http://localhost:8000/user/users?page=1&username__icontains=mah&search=81730

# --------=============== HOW TO USE FILTER END POINTS (django-url-filter) ===================---------#

    # http://localhost:8000/user/userfilter?id__in=2,4,5
    # http://localhost:8000/user/userfilter?username__contains=Mahi&email=mahi6535@gmail.com
    # http://localhost:8000/user/userfilter?email__icontians=mahi6535@gmail.com


