from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostulacionViewSet

router = DefaultRouter()
router.register(r'', PostulacionViewSet, basename='postulacion')

app_name = 'postulaciones'

urlpatterns = [
    path('', include(router.urls)),
]
