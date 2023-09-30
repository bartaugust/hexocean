from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from .models import UploadedImage
from .serializers import UploadedImageSerializer


class ImageViewSet(ViewSet):
    queryset = UploadedImage.objects.all()
    serializer_class = UploadedImageSerializer

# class ItemViewSet(ViewSet):
#     queryset = Item.objects.all()
#
#     def list(self, request):
#         serializer = ItemSerializer(self.queryset, many=True)
#         return Response(serializer.data)
#
#     def retrieve(self, request, pk=None):
#         item = get_object_or_404(self.queryset, pk=pk)
#         serializer = ItemSerializer(item)
#         return Response(serializer.data)
