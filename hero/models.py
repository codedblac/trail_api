from django.db import models


class HeroSlide(models.Model):
    """A single slide in the hero carousel."""

    # --------- TEXT CONTENT ---------
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    # --------- CTA (Call to Action) ---------
    cta_text = models.CharField(max_length=100, default="Shop Now")
    cta_link = models.URLField(max_length=300, blank=True, null=True)

    badge = models.CharField(max_length=100, blank=True, null=True)

    # --------- MEDIA ---------
    image = models.ImageField(
        upload_to="hero/slides/images/",
        blank=True,
        null=True,
        help_text="Main image for the slide"
    )
    mobile_image = models.ImageField(
        upload_to="hero/slides/mobile/",
        blank=True,
        null=True,
        help_text="Optional mobile-optimized image"
    )
    video = models.FileField(
        upload_to="hero/slides/videos/",
        blank=True,
        null=True,
        help_text="Optional background video"
    )

    # --------- DESIGN ---------
    bg_color = models.CharField(
        max_length=100,
        default="from-blue-600 to-purple-600",
        help_text="Tailwind gradient e.g. from-blue-600 to-purple-600"
    )
    overlay_color = models.CharField(
        max_length=50,
        default="black",
        help_text="Overlay color (CSS color)"
    )
    overlay_opacity = models.FloatField(
        default=0.4,
        help_text="Overlay opacity (0 = none, 1 = full)"
    )
    text_color = models.CharField(
        max_length=50,
        default="white",
        help_text="Text color (CSS)"
    )
    align = models.CharField(
        max_length=20,
        choices=[
            ("left", "Left"),
            ("center", "Center"),
            ("right", "Right"),
        ],
        default="left",
        help_text="Text alignment"
    )

    # --------- SETTINGS ---------
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    duration = models.PositiveIntegerField(
        default=5000,
        help_text="Slide duration in milliseconds"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "created_at"]

    def __str__(self):
        return f"{self.title} (#{self.order})"
