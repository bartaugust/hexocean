from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from .models import UploadedImage
from .serializers import UploadedImageSerializer


class ImageViewSet(ModelViewSet):
    serializer_class = UploadedImageSerializer

    # queryset = UploadedImage.objects.all()
    permission_classes = [IsAuthenticated]
    queryset = UploadedImage.objects.filter()

    def get_queryset(self):
        return UploadedImage.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # thumbnails = self.request.user.tier.thumbnail_sizes
        serializer.save(user=self.request.user)
