# products/urls.py
from django.urls import path
from .views import (
    # Products
    ProductListView,
    ProductDetailView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    # Categories
    CategoryListView,
    CategoryDetailView,
    CategoryCreateView,
    CategoryUpdateView,
    CategoryDeleteView,
    # Hero Banners
    HeroBannerListView,
    HeroBannerDetailView,
    HeroBannerCreateView,
    HeroBannerUpdateView,
    HeroBannerDeleteView,
)

urlpatterns = [
    # --------------------
    # Products
    # --------------------
    path("products/", ProductListView.as_view(), name="product-list"),
    path("products/<int:id>/", ProductDetailView.as_view(), name="product-detail"),
    path("products/create/", ProductCreateView.as_view(), name="product-create"),
    path("products/<int:id>/update/", ProductUpdateView.as_view(), name="product-update"),
    path("products/<int:id>/delete/", ProductDeleteView.as_view(), name="product-delete"),

    # --------------------
    # Categories
    # --------------------
    path("categories/", CategoryListView.as_view(), name="category-list"),
    path("categories/<int:id>/", CategoryDetailView.as_view(), name="category-detail"),
    path("categories/create/", CategoryCreateView.as_view(), name="category-create"),
    path("categories/<int:id>/update/", CategoryUpdateView.as_view(), name="category-update"),
    path("categories/<int:id>/delete/", CategoryDeleteView.as_view(), name="category-delete"),

    # --------------------
    # Hero Banners
    # --------------------
    path("hero-banners/", HeroBannerListView.as_view(), name="hero-banner-list"),
    path("hero-banners/<int:id>/", HeroBannerDetailView.as_view(), name="hero-banner-detail"),
    path("hero-banners/create/", HeroBannerCreateView.as_view(), name="hero-banner-create"),
    path("hero-banners/<int:id>/update/", HeroBannerUpdateView.as_view(), name="hero-banner-update"),
    path("hero-banners/<int:id>/delete/", HeroBannerDeleteView.as_view(), name="hero-banner-delete"),
]
