from rest_framework.routers import DefaultRouter
from .views import HeroSlideViewSet

router = DefaultRouter()
router.register(r'hero-slides', HeroSlideViewSet, basename='hero-slide')

urlpatterns = router.urls
