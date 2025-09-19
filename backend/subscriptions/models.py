from django.core.validators import MaxValueValidator
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Tariff(models.Model):
    name = models.CharField( max_length=111)
    discount_percent = models.PositiveIntegerField(default=0,
                                                   validators=[
                                                       MaxValueValidator(100)
                                                   ]
                                                   )

class UserSubscription(models.Model):
    follower = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        verbose_name="Подписчик",
        null=True,
        blank=True,
    )
    tariff = models.ForeignKey(Tariff, related_name="subscriptions", on_delete=models.PROTECT)
    is_active = models.BooleanField(default=False, verbose_name="Активна")

    def is_valid(self):
        return self.is_active
