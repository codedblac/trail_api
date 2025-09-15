from django.urls import path
from .views import (
    AnalyticsOverviewView,
    SalesOverTimeView,
    RecentOrdersView,
)

urlpatterns = [
    path("overview/", AnalyticsOverviewView.as_view(), name="analytics-overview"),
    path("sales/", SalesOverTimeView.as_view(), name="analytics-sales"),
    path("recent-orders/", RecentOrdersView.as_view(), name="analytics-recent-orders"),
]
