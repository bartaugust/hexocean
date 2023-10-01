from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from .models import UploadedImage
from .serializers import UploadedImageSerializer


class ImageViewSet(ModelViewSet):
    serializer_class = UploadedImageSerializer
    permission_classes = [IsAuthenticated]
    queryset = UploadedImage.objects.none()

    def get_queryset(self):
        return UploadedImage.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
