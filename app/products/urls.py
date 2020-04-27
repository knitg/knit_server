from django.urls import include, path
from rest_framework import routers
from . import views
from django.conf.urls import url

from .kviews.imageview import ImageViewSet
from .kviews.stitchview import StitchViewSet
from .kviews.csv_ref_stitch_view import CSVUploadStitchViewSet, CSVUploadStitchTypeViewSet
from .kviews.stitchtypeview import StitchTypeViewSet
from .kviews.offers_view import OffersViewSet
from .kviews.productview import ProductViewSet, ProductListViewSet
from .kviews.colors_view import ColorsViewSet
from .kviews.material_view import MaterialViewSet
from .kviews.sizes_view import SizesViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'upload', ImageViewSet)
router.register(r'csv-stitch', CSVUploadStitchViewSet, basename="csv-stitch")
router.register(r'csv-stitch-types', CSVUploadStitchTypeViewSet, basename="csv-stitch-types")
router.register(r'stitch', StitchViewSet, basename="stitch")
router.register(r'stitch-types', StitchTypeViewSet)
router.register(r'products', ProductViewSet)
router.register(r'product-list', ProductListViewSet)
router.register(r'offers', OffersViewSet)
router.register(r'colors', ColorsViewSet)
router.register(r'materials', MaterialViewSet)
router.register(r'sizes', SizesViewSet)

# router.register(r'userproducts/(?P<user_id>\d+)', ProductByUserViewSet)
# router.register(r'stitchproducts/(?P<stitch_id>\d+)', ProductByStitchViewSet)
# router.register(r'stitchtypeproducts/(?P<stitch_type_id>\d+)', ProductByStitchTypeViewSet)
# router.register(r'stitch-type/(?P<stitch_id>\d+)', StitchTypeByStitchViewSet)

urlpatterns = [ 
    path('', include(router.urls))
]
