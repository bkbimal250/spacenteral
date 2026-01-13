from rest_framework.routers import DefaultRouter
from .views import SimCardViewSet

router = DefaultRouter()
router.register(r'simcards', SimCardViewSet, basename='simcard')

urlpatterns = router.urls
