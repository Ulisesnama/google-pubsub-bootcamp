from django.contrib import admin

from .models import Item, Stock

# Register your models here.
admin.site.register(Item)
admin.site.register(Stock)
