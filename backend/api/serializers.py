from django.contrib.auth.validators import ASCIIUsernameValidator
from django.db import transaction
from rest_framework import serializers

from subscriptions.models import UserSubscription, Tariff
from products.models import Product, Order, ProductOrder

from users.models import CustomUser

class UserSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSubscription
        fields = '__all__'


class TariffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tariff
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'



class ProductOrderSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = ProductOrder
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    products = ProductOrderSerializer(source='order_with_products', many=True, read_only=True)
    customer_username = serializers.CharField(source='customer.username', read_only=True)

    class Meta:
        model = Order
        fields = '__all__'


class OrderCreateSerializer(serializers.ModelSerializer):
    products = serializers.ListField(
        child=serializers.DictField(),
        write_only=True,
        required=True
    )

    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        products_data = validated_data.pop('products')
        order = Order.objects.create(**validated_data)

        total_amount = 0
        for product_data in products_data:
            product = Product.objects.get(id=product_data['product_id'])
            quantity = product_data.get('quantity', 1)

            ProductOrder.objects.create(
                order=order,
                product=product,
                quantity=quantity
            )


            total_amount += product.price * quantity

        order.total_amount = total_amount
        order.save()
        return order


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, max_length=150)
    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=[
            ASCIIUsernameValidator(),
        ],
    )
    password = serializers.CharField(required=True,
                                     max_length=150,
                                     write_only=True)

    class Meta:
        model = CustomUser
        fields = [
            "email",
            "username",
            "password",
            "id",
        ]
        extra_kwargs = {"password": {"write_only": True}}

