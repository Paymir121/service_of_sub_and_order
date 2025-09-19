from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (UserSubscriptionViewsSet, TariffViewSet, OrderViewSet, ProductViewSet)

app_name = "api"

router_v1 = DefaultRouter()
router_v1.register("subscriptions", UserSubscriptionViewsSet, basename="subscriptions")
router_v1.register("tarrifs", TariffViewSet, basename="tarrifs")
router_v1.register("products", ProductViewSet, basename="products")
router_v1.register('orders', OrderViewSet, basename="orders")

urlpatterns = [
    path("", include(router_v1.urls)),
    path("", include("djoser.urls")),
    path("auth/", include("djoser.urls.authtoken")),
]