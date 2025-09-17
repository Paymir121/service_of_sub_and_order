from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (UserSubscriptionViewsSet, TariffViewSet, ProductViewSet)

app_name = "api"

router_v1 = DefaultRouter()
router_v1.register("users", UserSubscriptionViewsSet, basename="subscription")
router_v1.register("tags", TariffViewSet, basename="tarrif")
router_v1.register("tags", ProductViewSet, basename="products")

urlpatterns = [
    path("", include(router_v1.urls)),
]