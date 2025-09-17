from django.db import transaction
from rest_framework import serializers

from subscription.models import UserSubscription, Tariff
from products.models import Product

class UserSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSubscription
        fields = ("__all__")


class TariffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tariff
        fields = ("__all__")

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("__all__")