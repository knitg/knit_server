from django.urls import include, path
from rest_framework import routers
from . import views
from django.conf.urls import url

from .kviews.order_image_view import OrderImageViewSet
from .kviews.request_masters_view import RequestMasterViewSet
from .kviews.stitch_order_view import StitchOrderViewSet
from .kviews.product_order_view import ProductOrderViewSet

router = routers.DefaultRouter(trailing_slash=False) 
router.register(r'product', ProductOrderViewSet)
router.register(r'stitch', StitchOrderViewSet)
router.register(r'master', RequestMasterViewSet)
router.register(r'image', OrderImageViewSet) 

urlpatterns = [ 
    path('', include(router.urls))
]
