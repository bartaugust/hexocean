from rest_framework import serializers
from .models import UploadedImage


class UploadedImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedImage
        fields = ('id', 'image')

    def to_representation(self, instance):

        user = self.context['request'].user
        data = super(UploadedImageSerializer, self).to_representation(instance)

        data['thumbnails'] = user.tier.thumbnail_sizes
        if user.is_authenticated:
            if not user.tier.is_link_present:
                data.pop('image')
        return data
