# products/filters.py
import django_filters
from django.db.models import Q
from rest_framework.filters import OrderingFilter
from .models import Product, Category, HeroBanner


# ----------------------------
# PRODUCT FILTER
# ----------------------------
class ProductFilter(django_filters.FilterSet):
    # Price range filter
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr='lte')
    
    # Category filter (by slug or ID)
    category = django_filters.CharFilter(method='filter_by_category')
    
    # Search by name, description, SKU
    search = django_filters.CharFilter(method='filter_by_search')

    class Meta:
        model = Product
        fields = ['is_featured', 'is_on_sale', 'category']

    def filter_by_category(self, queryset, name, value):
        # Allow filter by slug or numeric ID
        if value.isdigit():
            return queryset.filter(category__id=value)
        return queryset.filter(category__slug=value)

    def filter_by_search(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) |
            Q(description__icontains=value) |
            Q(sku__icontains=value)
        )


# ----------------------------
# CATEGORY FILTER
# ----------------------------
class CategoryFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Category
        fields = ['is_active', 'search']


# ----------------------------
# HERO / BANNER FILTER
# ----------------------------
class HeroBannerFilter(django_filters.FilterSet):
    is_active = django_filters.BooleanFilter(field_name='is_active')

    class Meta:
        model = HeroBanner
        fields = ['is_active', 'display_order']
