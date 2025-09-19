from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse


def health_check(request):
    """Simple health check endpoint"""
    return JsonResponse({"status": "ok", "message": "Adfinitum Backend is running"})


urlpatterns = [
    # Django Admin
    path("admin/", admin.site.urls),

    # API endpoints without versioning
    path("api/accounts/", include(("accounts.urls", "accounts"), namespace="accounts")),
    path("api/products/", include(("products.urls", "products"), namespace="products")),
    path("api/cart/", include(("cart.urls", "cart"), namespace="cart")),
    path("api/orders/", include(("orders.urls", "orders"), namespace="orders")),
    path("api/payments/", include(("payments.urls", "payments"), namespace="payments")),
    path("api/shipping/", include(("shipping.urls", "shipping"), namespace="shipping")),
    path("api/hero/", include(("hero.urls", "hero"), namespace="hero")),
    path("api/analytics/", include(("analytics.urls", "analytics"), namespace="analytics")),

    # Health check
    path("api/health/", health_check, name="health-check"),
]

# Serve static/media in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
