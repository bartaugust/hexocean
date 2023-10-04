from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ImageViewSet, ImageFromLinkView

router = DefaultRouter()
router.register(r'images', ImageViewSet, basename='images')


urlpatterns = [
    path('', include(router.urls)),
    path('link/<str:token>/', ImageFromLinkView.as_view(), name='image_from_link'),
]
