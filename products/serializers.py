# products/serializers.py
from rest_framework import serializers
from .models import (
    Category,
    Product,
    ProductImage,
    ProductVariation,
    HeroBanner,
)


# ----------------------------
# CATEGORY SERIALIZER
# ----------------------------
class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'parent', 'description', 'is_active', 'subcategories']

    def get_subcategories(self, obj):
        subs = obj.subcategories.filter(is_active=True)
        return CategorySerializer(subs, many=True, read_only=True).data


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
        fields = ['id', 'name', 'sku', 'price', 'stock_quantity', 'is_active']


# ----------------------------
# PRODUCT SERIALIZER
# ----------------------------
class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    variations = ProductVariationSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.filter(is_active=True), source='category', write_only=True
    )

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
            'sku',
            'seo_title',
            'seo_description',
            'category',
            'category_id',
            'images',
            'variations',
        ]
        read_only_fields = ['slug', 'is_on_sale', 'is_featured']


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
