from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from subscription.models import UserSubscription, Tariff
from products.models import Product

from .serializers import UserSubscriptionSerializer, TariffSerializer, ProductSerializer


class UserSubscriptionViewsSet(ModelViewSet):
    pagination_class = None
    lookup_field = "id"
    queryset = UserSubscription.objects.all()
    serializer_class = UserSubscriptionSerializer

class TariffViewSet(ModelViewSet):
    pagination_class = None
    lookup_field = "id"
    queryset = Tariff.objects.all()
    serializer_class = TariffSerializer

class ProductViewSet(ModelViewSet):
    pagination_class = None
    lookup_field = "id"
    queryset = Product.objects.all()
    serializer_class = ProductSerializer