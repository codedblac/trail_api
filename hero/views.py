from rest_framework import viewsets, permissions
from .models import HeroSlide
from .serializers import HeroSlideSerializer


class HeroSlideViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing Hero Slides.
    - Admins can create/update/delete
    - Public can only read active slides
    """
    serializer_class = HeroSlideSerializer
    permission_classes = [permissions.AllowAny]  # Allow read-only for public

    def get_queryset(self):
        """
        If user is admin → return all slides.
        Otherwise → return only active slides, ordered by 'order'.
        """
        if self.request.user.is_staff:
            return HeroSlide.objects.all().order_by("order")
        return HeroSlide.objects.filter(is_active=True).order_by("order")
