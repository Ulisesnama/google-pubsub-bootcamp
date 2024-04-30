from rest_framework.serializers import (ChoiceField, ModelSerializer,
                                        ValidationError)

from .models import Item, Stock


class ItemSerializer(ModelSerializer):
    class Meta:
        model = Item
        fields = ["id", "name", "description"]


class StockSerializer(ModelSerializer):
    action = ChoiceField(choices=["add", "subtract"], write_only=True)

    class Meta:
        model = Stock
        fields = ["item", "quantity", "action"]

    def validate(self, data):
        action = data.get("action")
        quantity = data.get("quantity", 0)

        if action == "subtract" and self.instance:
            if self.instance.quantity < quantity:
                raise ValidationError(
                    "You cannot remove more stock than what is available."
                )
        return data
