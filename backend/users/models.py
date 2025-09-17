from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.db import models


class CustomUser(AbstractUser):

    bio = models.TextField("Биография", null=False, blank=True)
    username = models.CharField(
        unique=True,
        max_length=150,
        validators=[
            ASCIIUsernameValidator(),
        ],
    )
    first_name = models.CharField(
        max_length=150,
    )
    last_name = models.CharField(
        max_length=150,
    )
    password = models.CharField(
        max_length=150,
    )
    email = models.EmailField(
        verbose_name="email address",
        max_length=254, unique=True)

    phone = models.CharField(
        max_length=13,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["username", "email"],
                name="unique_user")
        ]
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username
