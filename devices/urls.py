# pyrefly: ignore [missing-import]
from rest_framework.routers import DefaultRouter
from .views import DeviceViewSet, UtensilViewSet

router = DefaultRouter()
router.register(r'devices', DeviceViewSet, basename='device')
router.register(r'utensils', UtensilViewSet, basename='utensil')

urlpatterns = router.urls
