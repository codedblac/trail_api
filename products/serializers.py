from rest_framework import serializers
from .models import (
    Category,
    Product,
    ProductImage,
    ProductVariation,
    HeroBanner,
    Brand,
    ProductReview,
)


# ----------------------------
# CATEGORY SERIALIZER
# ----------------------------
class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'slug',
            'parent',
            'description',
            'is_active',
            'subcategories',
        ]

    def get_subcategories(self, obj):
        subs = obj.subcategories.filter(is_active=True)
        return CategorySerializer(subs, many=True, read_only=True).data


# ----------------------------
# BRAND SERIALIZER
# ----------------------------
class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name', 'slug', 'description', 'is_active']


# ----------------------------
# PRODUCT IMAGE SERIALIZER
# ----------------------------
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'alt_text', 'is_featured']


# ----------------------------
# PRODUCT VARIATION SERIALIZER
# ----------------------------
class ProductVariationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariation
        fields = [
            'id',
            'name',
            'sku',
            'price',
            'stock_quantity',
            'is_active',
        ]


# ----------------------------
# PRODUCT REVIEW SERIALIZER
# ----------------------------
class ProductReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.full_name", read_only=True)

    class Meta:
        model = ProductReview
        fields = [
            'id',
            'user',
            'user_name',
            'rating',
            'comment',
            'created_at',
        ]
        read_only_fields = ['id', 'user', 'user_name', 'created_at']


# ----------------------------
# PRODUCT SERIALIZER
# ----------------------------
class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    variations = ProductVariationSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.filter(is_active=True),
        source='category',
        write_only=True
    )
    brand = BrandSerializer(read_only=True)
    brand_id = serializers.PrimaryKeyRelatedField(
        queryset=Brand.objects.filter(is_active=True),
        source="brand",
        write_only=True,
        required=False
    )
    rating = serializers.FloatField(source="average_rating", read_only=True)
    review_count = serializers.IntegerField(source="review_count", read_only=True)
    reviews = ProductReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'slug',
            'description',
            'price',
            'discount_price',
            'is_on_sale',
            'is_featured',
            'stock_quantity',
            'availability',
            'sku',
            'seo_title',
            'seo_description',
            'category',
            'category_id',
            'brand',
            'brand_id',
            'images',
            'variations',
            'rating',
            'review_count',
            'reviews',
        ]
        read_only_fields = [
            'slug',
            'is_on_sale',
            'is_featured',
            'rating',
            'review_count',
        ]


# ----------------------------
# HERO / BANNER SERIALIZER
# ----------------------------
class HeroBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeroBanner
        fields = [
            'id',
            'title',
            'subtitle',
            'image',
            'cta_text',
            'cta_link',
            'is_active',
            'display_order',
        ]
