from django.contrib.auth.validators import ASCIIUsernameValidator
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserProfileManager(BaseUserManager):
    """Class required by Django for managing our users from the management
    command.
    """

    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address.')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email,
            username,
            password
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractUser):

    bio = models.TextField("Биография", null=False, blank=True)
    username = models.CharField(
        unique=True,
        max_length=150,
        blank=True,
        null=True
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
    telegram_id = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    objects = UserProfileManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username




