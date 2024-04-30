from google.api_core.exceptions import GoogleAPIError
from google.cloud import pubsub_v1
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Item, Stock
from .serializers import ItemSerializer, StockSerializer


class ItemViewSet(ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class StockViewSet(ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    publisher = pubsub_v1.PublisherClient()

    def partial_update(self, request: Request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if not serializer.is_valid(raise_exception=True):
            return Response(
                {"status": "BAD_REQUEST", "data": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        action = serializer.validated_data.get("action")
        quantity = serializer.validated_data.get("quantity")

        if action == "add":
            instance.quantity += quantity
        elif action == "subtract":
            instance.quantity -= quantity

        instance.save()
        updated_serializer = self.get_serializer(instance)

        try:
            if updated_serializer.data["quantity"] < 5:
                topic_path = self.publisher.topic_path("testing-pubsub", "stock")
                message_json = {
                    "id": instance.item.id,
                    "name": instance.item.name,
                    "stock": instance.quantity,
                }
                message_data = str(message_json).encode("utf-8")
                future = self.publisher.publish(topic_path, message_data)
                print(f"Future: {future.result()}")

        except GoogleAPIError as e:
            print(f"Future error: {e}")

        return Response(
            {"status": "OK", "data": updated_serializer.data},
            status=status.HTTP_200_OK,
        )
