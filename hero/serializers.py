from rest_framework import serializers
from .models import HeroSlide


class HeroSlideSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    mobile_image = serializers.SerializerMethodField()
    video = serializers.SerializerMethodField()

    class Meta:
        model = HeroSlide
        fields = [
            "id",
            "title",
            "subtitle",
            "description",
            "cta_text",
            "cta_link",
            "badge",
            "image",
            "mobile_image",
            "video",
            "bg_color",
            "overlay_color",
            "overlay_opacity",
            "text_color",
            "align",
            "is_active",
            "order",
            "duration",
        ]

    # Convert image paths to full URLs
    def get_image(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.image.url) if obj.image else None

    def get_mobile_image(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.mobile_image.url) if obj.mobile_image else None

    def get_video(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.video.url) if obj.video else None
