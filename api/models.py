from django.core.validators import MinValueValidator
from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    objects = models.Manager()

    def __str__(self):
        return self.name


class Stock(models.Model):
    item = models.OneToOneField(
        Item, on_delete=models.CASCADE, related_name="stock", primary_key=True
    )
    quantity = models.IntegerField(validators=[MinValueValidator(1)])

    objects = models.Manager()

    def __str__(self):
        return f"{self.item.name} - Stock: {self.quantity}"
