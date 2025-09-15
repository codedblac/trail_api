from django.db.models import Sum, Count
from django.utils.timezone import now, timedelta

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from orders.models import Order
from products.models import Product
from accounts.models import CustomUser


# ---------------------------
# Dashboard Overview
# ---------------------------
class AnalyticsOverviewView(APIView):
    """
    Returns key metrics for the admin dashboard.
    """
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        total_revenue = Order.objects.filter(status="completed").aggregate(
            total=Sum("total_amount")
        )["total"] or 0

        total_orders = Order.objects.count()
        total_products = Product.objects.count()
        total_customers = CustomUser.objects.filter(role="customer").count()

        data = {
            "total_revenue": total_revenue,
            "total_orders": total_orders,
            "total_products": total_products,
            "total_customers": total_customers,
        }
        return Response(data)


# ---------------------------
# Sales Over Time
# ---------------------------
class SalesOverTimeView(APIView):
    """
    Returns sales totals grouped by day (last 30 days).
    """
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        start_date = now() - timedelta(days=30)

        sales = (
            Order.objects.filter(created_at__gte=start_date, status="completed")
            .extra(select={"day": "date(created_at)"})
            .values("day")
            .annotate(total=Sum("total_amount"), count=Count("id"))
            .order_by("day")
        )

        return Response(sales)


# ---------------------------
# Recent Orders
# ---------------------------
class RecentOrdersView(APIView):
    """
    Returns the latest 10 orders for quick view.
    """
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        recent_orders = (
            Order.objects.select_related("user")
            .order_by("-created_at")[:10]
            .values(
                "id",
                "user__email",
                "status",
                "total_amount",
                "created_at",
            )
        )
        return Response(recent_orders)
