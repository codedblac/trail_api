from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg, Q
from .models import Product, Category, HeroBanner, Brand, ProductReview
from .serializers import (
    ProductSerializer,
    CategorySerializer,
    HeroBannerSerializer,
    BrandSerializer,
    ProductReviewSerializer,
)


# ------------------------------
# Products
# ------------------------------
class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "description", "sku"]
    ordering_fields = ["price", "created_at", "updated_at", "avg_rating"]
    ordering = ["-created_at"]

    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True).annotate(
            avg_rating=Avg("reviews__rating")
        )
        params = self.request.query_params

        # --- Multi-select filters (comma-separated) ---
        brand = params.get("brand")
        if brand:
            values = [b.strip() for b in brand.split(",")]
            if all(v.isdigit() for v in values):
                queryset = queryset.filter(brand_id__in=values)
            else:
                queryset = queryset.filter(brand__name__in=values)

        category = params.get("category")
        if category:
            values = [c.strip() for c in category.split(",")]
            if all(v.isdigit() for v in values):
                queryset = queryset.filter(category_id__in=values)
            else:
                queryset = queryset.filter(category__name__in=values)

        availability = params.get("availability")
        if availability:
            statuses = [a.strip() for a in availability.split(",")]
            queryset = queryset.filter(availability__in=statuses)

        # --- Price range ---
        min_price = params.get("min_price")
        max_price = params.get("max_price")
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        # --- Minimum rating ---
        min_rating = params.get("min_rating")
        if min_rating:
            queryset = queryset.filter(avg_rating__gte=min_rating)

        # --- Sorting (frontend sends `sort` param) ---
        sort = params.get("sort")
        if sort == "price-low":
            queryset = queryset.order_by("price")
        elif sort == "price-high":
            queryset = queryset.order_by("-price")
        elif sort == "newest":
            queryset = queryset.order_by("-created_at")
        elif sort == "rating":
            queryset = queryset.order_by("-avg_rating")

        return queryset


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = "slug"   # Use slug for SEO


class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAdminUser]


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
# Product Reviews
# ------------------------------
class ProductReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = ProductReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        product_id = self.kwargs.get("product_id")
        return ProductReview.objects.filter(product_id=product_id)

    def perform_create(self, serializer):
        product_id = self.kwargs.get("product_id")
        serializer.save(user=self.request.user, product_id=product_id)


# ------------------------------
# Categories
# ------------------------------
class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.filter(is_active=True)
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
# Brands
# ------------------------------
class BrandListView(generics.ListAPIView):
    queryset = Brand.objects.filter(is_active=True)
    serializer_class = BrandSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["name"]
    ordering = ["name"]


class BrandDetailView(generics.RetrieveAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = "id"


# ------------------------------
# Hero Banners / Ads
# ------------------------------
class HeroBannerListView(generics.ListAPIView):
    queryset = HeroBanner.objects.filter(is_active=True).order_by("display_order", "-created_at")
    serializer_class = HeroBannerSerializer
    permission_classes = [permissions.AllowAny]


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
