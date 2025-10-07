from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MachineViewSet, MachineAssignmentViewSet

router = DefaultRouter()
router.register(r'machines', MachineViewSet, basename='machine')
router.register(r'machine-assignments', MachineAssignmentViewSet, basename='machine-assignment')

urlpatterns = [
    path('', include(router.urls)),
]


