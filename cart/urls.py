from django.urls import path
from .views import CartViewSet

cart_list = CartViewSet.as_view({
    "get": "list",
})

urlpatterns = [
    path("cart/", cart_list, name="cart-detail"),
    path("cart/items/", CartViewSet.as_view({"post": "add_item"}), name="cart-add-item"),
    path("cart/items/<int:pk>/", CartViewSet.as_view({
        "patch": "update_item",
        "delete": "remove_item",
    }), name="cart-manage-item"),
    path("cart/clear/", CartViewSet.as_view({"post": "clear"}), name="cart-clear"),
    path("cart/apply-coupon/", CartViewSet.as_view({"post": "apply_coupon"}), name="cart-apply-coupon"),
]
