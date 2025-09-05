# products/views.py
from rest_framework import generics, permissions, filters
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product, Category, HeroBanner
from .serializers import ProductSerializer, CategorySerializer, HeroBannerSerializer


# ------------------------------
# Products
# ------------------------------
class ProductListView(generics.ListAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]  # Public endpoint
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["category", "is_active", "price"]
    search_fields = ["name", "description"]
    ordering_fields = ["price", "created_at", "updated_at"]
    ordering = ["-created_at"]


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = "id"


class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAdminUser]  # Admin only


class ProductUpdateView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = "id"


class ProductDeleteView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = "id"


# ------------------------------
# Categories
# ------------------------------
class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["name"]
    ordering = ["name"]


class CategoryDetailView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = "id"


class CategoryCreateView(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]


class CategoryUpdateView(generics.UpdateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = "id"


class CategoryDeleteView(generics.DestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = "id"


# ------------------------------
# Hero Banners / Ads
# ------------------------------
class HeroBannerListView(generics.ListAPIView):
    queryset = HeroBanner.objects.filter(is_active=True)
    serializer_class = HeroBannerSerializer
    permission_classes = [permissions.AllowAny]
    ordering = ["-created_at"]


class HeroBannerDetailView(generics.RetrieveAPIView):
    queryset = HeroBanner.objects.filter(is_active=True)
    serializer_class = HeroBannerSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = "id"


class HeroBannerCreateView(generics.CreateAPIView):
    queryset = HeroBanner.objects.all()
    serializer_class = HeroBannerSerializer
    permission_classes = [permissions.IsAdminUser]


class HeroBannerUpdateView(generics.UpdateAPIView):
    queryset = HeroBanner.objects.all()
    serializer_class = HeroBannerSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = "id"


class HeroBannerDeleteView(generics.DestroyAPIView):
    queryset = HeroBanner.objects.all()
    serializer_class = HeroBannerSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = "id"
