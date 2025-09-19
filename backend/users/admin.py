from django.contrib import admin

from .models import  CustomUser


@admin.register(CustomUser)
class Users(admin.ModelAdmin):
    list_display = ("email", "username",)
    search_fields = ("email__startswith", "username__startswith")
