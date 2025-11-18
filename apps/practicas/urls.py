from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PracticaViewSet

router = DefaultRouter()
router.register(r'', PracticaViewSet, basename='practica')

app_name = 'practicas'

urlpatterns = [
    path('', include(router.urls)),
]
