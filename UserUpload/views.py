from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import UploadedImage, ExpiringLink
from .serializers import UploadedImageSerializer, ExpiringLinkSerializer

from django.shortcuts import get_object_or_404


class ImageViewSet(ModelViewSet):
    serializer_class = UploadedImageSerializer
    permission_classes = [IsAuthenticated]
    queryset = UploadedImage.objects.none()

    def get_serializer_class(self):
        # Use a different serializer for a custom action
        if self.action == 'generate_expiring_link':
            return ExpiringLinkSerializer
        return UploadedImageSerializer

    def get_queryset(self):
        return UploadedImage.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['get', 'post'], url_path='generate-expiring-link')
    def generate_expiring_link(self, request, pk):
        image = self.get_object()

        if request.method == 'GET':
            links = ExpiringLink.objects.filter(image=image)
            serializer = self.get_serializer(links, many=True)
        if request.method == 'POST':
            serializer = ExpiringLinkSerializer(data=request.data)
            if serializer.is_valid():
                validated_data = serializer.validated_data
                ExpiringLink.objects.create(**validated_data, image=image)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        return Response(serializer.data)
