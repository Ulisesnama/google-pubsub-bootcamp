from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Item, Stock


@receiver(post_save, sender=Item)
def create_stock(sender, instance, created, **kwargs):
    if created:
        Stock.objects.create(item=instance, quantity=0)
