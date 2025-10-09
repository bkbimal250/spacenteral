from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MachineViewSet, AccountHolderViewSet

router = DefaultRouter()
router.register(r'machines', MachineViewSet, basename='machine')
router.register(r'account-holders', AccountHolderViewSet, basename='account-holder')

urlpatterns = [
    path('', include(router.urls)),
]


