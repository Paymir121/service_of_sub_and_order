from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
import requests
from django.conf import settings

User = get_user_model()

class Product(models.Model):

    name = models.CharField(
        max_length=256,
        verbose_name="Название продукта",
        help_text="Введите название продукта",
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Цена"
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
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Общая сумма"
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.send_order_id_to_telegram_bot()

    def send_order_id_to_telegram_bot(self):
        print(f"send_order_post_request")
        BOT_SERVER_URL: str = f"http://telegram_bot:8080/get_order/{self.id}/"
        try:
            response = requests.get(
                BOT_SERVER_URL,
                headers={'Content-Type': 'application/json'},
            )

            if response.status_code not in [200, 201]:
                print(f"Ошибка при отправке заказа: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Ошибка при обработке заказа: {e}")

class ProductOrder(models.Model):
    product = models.ForeignKey(Product, related_name="products_in_order", on_delete=models.PROTECT)
    order = models.ForeignKey(Order, related_name="order_with_products", on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name="Количество"
    )


