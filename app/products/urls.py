from django.urls import include, path
from rest_framework import routers
from . import views
from django.conf.urls import url

from .kviews.imageview import ImageViewSet
from .kviews.stitchview import StitchViewSet
from .kviews.stitchtypeview import StitchTypeViewSet
from .kviews.stitchdesignview import StitchTypeDesignViewSet
from .kviews.prices_view import PricesViewSet
from .kviews.offers_view import OffersViewSet
from .kviews.productview import ProductViewSet, ProductByUserViewSet, ProductByStitchViewSet, ProductByStitchTypeViewSet
from .kviews.colors_view import ColorsViewSet
from .kviews.sizes_view import SizesViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'upload', ImageViewSet)
router.register(r'stitch', StitchViewSet)
router.register(r'stitch-types', StitchTypeViewSet)
router.register(r'stitch-type-design', StitchTypeDesignViewSet)
router.register(r'product', ProductViewSet)
router.register(r'prices', PricesViewSet)
router.register(r'offers', OffersViewSet) 
router.register(r'colors', ColorsViewSet) 
router.register(r'sizes', SizesViewSet)

# router.register(r'userproducts/(?P<user_id>\d+)', ProductByUserViewSet)
# router.register(r'stitchproducts/(?P<stitch_id>\d+)', ProductByStitchViewSet)
# router.register(r'stitchtypeproducts/(?P<stitch_type_id>\d+)', ProductByStitchTypeViewSet)
# router.register(r'stitch-type/(?P<stitch_id>\d+)', StitchTypeByStitchViewSet)

urlpatterns = [ 
    path('', include(router.urls))
]
