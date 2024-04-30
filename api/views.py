from google.api_core.exceptions import GoogleAPIError
from google.cloud import pubsub_v1
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from ast import literal_eval
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


class ReceiveLowItemStockViews(APIView):
    subscriber = pubsub_v1.SubscriberClient()

    def get(self, request: Request, *args, **kwargs):
        subscription_path = self.subscriber.subscription_path(
            "testing-pubsub", "stock-subscription"
        )
        response = self.subscriber.pull(
            request={"subscription": subscription_path, "max_messages": 10}
        )
        ack_ids = []
        items = []
        for received_message in response.received_messages:
            item_data = received_message.message.data.decode("utf-8")
            items.append(literal_eval(item_data))
            ack_ids.append(received_message.ack_id)

        if ack_ids:
            self.subscriber.acknowledge(
                request={"subscription": subscription_path, "ack_ids": ack_ids}
            )

        return Response(
            {"status": "OK", "data": items},
            status=status.HTTP_200_OK,
        )
