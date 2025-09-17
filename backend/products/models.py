from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Product(models.Model):

    name = models.CharField(
        max_length=256,
        verbose_name="Название продукта",
        help_text="Введите название продукта",
    )


class Order(models.Model):
    customer = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        verbose_name="Заказчик",
        null=True,
        blank=True,
    )
    products = models.ManyToManyField(
        Product,
        through="ProductOrder")

class ProductOrder(models.Model):
    product = models.ForeignKey(Product, related_name="products_in_order", on_delete=models.PROTECT)
    order = models.ForeignKey(Order, related_name="order_with_products", on_delete=models.PROTECT)
