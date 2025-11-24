from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EntregableViewSet

router = DefaultRouter()
router.register(r'entregables', EntregableViewSet, basename='entregable')

urlpatterns = [
    path('', include(router.urls)),
]
