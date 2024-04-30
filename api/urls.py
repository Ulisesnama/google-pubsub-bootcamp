from django.urls import path

from .views import ItemViewSet, ReceiveLowItemStockViews, StockViewSet

urlpatterns = [
    path("items/", ItemViewSet.as_view({"get": "list", "post": "create"})),
    path(
        "items/<int:pk>/",
        ItemViewSet.as_view(
            {"get": "retrieve", "patch": "partial_update", "delete": "destroy"}
        ),
    ),
    path("stock/", StockViewSet.as_view({"get": "list"})),
    path("stock/<int:pk>/", StockViewSet.as_view({"patch": "partial_update"})),
    path("low-stock/", ReceiveLowItemStockViews.as_view()),
]
