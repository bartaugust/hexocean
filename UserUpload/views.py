from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from django.core import signing
from django.http import HttpResponse

import uuid

from .models import UploadedImage, ExpiringLink
from .serializers import UploadedImageSerializer, ExpiringLinkSerializer
from .permissions import CanGenerateLink


class ImageViewSet(ModelViewSet):
    serializer_class = UploadedImageSerializer
    permission_classes = [IsAuthenticated]
    queryset = UploadedImage.objects.none()

    def get_serializer_class(self):
        if self.action == 'generate_expiring_link':
            return ExpiringLinkSerializer
        return UploadedImageSerializer

    def get_queryset(self):
        return UploadedImage.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['get', 'post'], url_path='generate-expiring-link',
            permission_classes=[CanGenerateLink])
    def generate_expiring_link(self, request, pk):
        def create_expiring_link(validated_data, image):
            id = uuid.uuid4()
            signed_link = signing.dumps(str(id))
            link = self.request.build_absolute_uri(f'/api/link/{signed_link}')
            ExpiringLink.objects.create(**validated_data, image=image, id=id, link=link)

        image = self.get_object()

        if request.method == 'GET':
            links = ExpiringLink.objects.filter(image=image)
            serializer = self.get_serializer(links, many=True)
        if request.method == 'POST':
            serializer = ExpiringLinkSerializer(data=request.data)
            if serializer.is_valid():
                validated_data = serializer.validated_data
                create_expiring_link(validated_data, image)

            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data)


class ImageFromLinkView(APIView):
    def get(self, request, token):
        link_id = signing.loads(token)
        expiring_link = ExpiringLink.objects.get(id=link_id)
        if expiring_link.is_expired():
            expiring_link.delete()
            return Response({"error": "The link has expired."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            image = expiring_link.image.image
            content_type = 'image/jpeg' if image.name.lower().endswith('.jpg') else 'image/png'
            return HttpResponse(image.read(), content_type=content_type)
        except ValueError:
            return