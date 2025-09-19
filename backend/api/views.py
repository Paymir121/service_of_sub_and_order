from rest_framework import  status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from subscriptions.models import UserSubscription, Tariff
from products.models import Product, ProductOrder, Order
from .serializers import UserSubscriptionSerializer, TariffSerializer, ProductSerializer, OrderSerializer, \
    OrderCreateSerializer


class UserSubscriptionViewsSet(ModelViewSet):
    queryset = UserSubscription.objects.all()
    serializer_class = UserSubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserSubscription.objects.filter(follower=self.request.user)

    def perform_create(self, serializer):
        serializer.save(follower=self.request.user)

    def perform_update(self, serializer):
        if 'follower' in serializer.validated_data:
            serializer.validated_data.pop('follower')
        serializer.save()

class TariffViewSet(ReadOnlyModelViewSet):
    queryset = Tariff.objects.all()
    serializer_class = TariffSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class OrderViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(customer=user)

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return OrderCreateSerializer
        return OrderSerializer

    def perform_create(self, serializer):
        if serializer.validated_data.get('customer') is None:
            serializer.save(customer=self.request.user)
        else:
            serializer.save()

    @action(detail=True, methods=['post'])
    def add_product(self, request, pk=None):
        order = self.get_object()
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)

        try:
            product = Product.objects.get(id=product_id)
            ProductOrder.objects.create(
                order=order,
                product=product,
                quantity=quantity
            )
            return Response({'status': 'product added'})
        except Exception as e:
            return Response(
                {'error': e},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=['post'])
    def remove_product(self, request, pk=None):
        order = self.get_object()
        product_id = request.data.get('product_id')

        try:
            product_order = ProductOrder.objects.get(
                order=order,
                product_id=product_id
            )
            product_order.delete()
            return Response({'status': 'product removed'})
        except Exception as e:
            return Response(
                {'error': e},
                status=status.HTTP_404_NOT_FOUND
            )