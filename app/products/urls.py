from django.urls import include, path
from rest_framework import routers
from . import views
from django.conf.urls import url

from .kviews.imageview import ImageViewSet
from .kviews.category_view import CategoryViewSet
from .kviews.csv_product_ref_tables_view import CSVUploadCategoryViewSet, CSVUploadSubCategoryViewSet, CSVUploadProductRefTblViewSet
from .kviews.sub_category_view import SubCategoryViewSet
from .kviews.offers_view import OffersViewSet
from .kviews.productview import ProductViewSet, ProductListViewSet
from .kviews.colors_view import ColorsViewSet
from .kviews.material_view import MaterialViewSet
from .kviews.sizes_view import SizesViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'upload', ImageViewSet)
router.register(r'csv-categorys', CSVUploadCategoryViewSet, basename="csv-categorys")
router.register(r'csv-sub-categorys', CSVUploadSubCategoryViewSet, basename="csv-sub-categorys")
router.register(r'csv-product-ref-tables', CSVUploadProductRefTblViewSet, basename="csv-product-ref-tables")
router.register(r'categorys', CategoryViewSet, basename="categorys")
router.register(r'sub-categorys', SubCategoryViewSet)
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
