from django.contrib import admin

from subscriptions.models import UserSubscription, Tariff

# Register your models here.
admin.site.register(Tariff)
admin.site.register(UserSubscription)
