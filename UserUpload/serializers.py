from rest_framework import serializers
from .models import UploadedImage, ExpiringLink
from sorl.thumbnail import get_thumbnail


class ExpiringLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpiringLink
        fields = ('id', 'expiry_time', 'link')


class UploadedImageSerializer(serializers.ModelSerializer):
    image_detail = serializers.HyperlinkedIdentityField(view_name='images-detail',
                                                        lookup_field='pk')

    class Meta:
        model = UploadedImage
        fields = ('id', 'image', 'image_detail')

    def to_representation(self, instance):
        request = self.context.get('request')
        user = self.context['request'].user
        data = super(UploadedImageSerializer, self).to_representation(instance)
        if user.is_authenticated:

            data['thumbnails'] = {}
            for size in user.tier.thumbnail_sizes:
                thumbnail = get_thumbnail(instance.image, f'{size}x{size}', crop='center', quality=99).url
                data['thumbnails'][size] = request.build_absolute_uri(thumbnail)
            if not user.tier.is_link_present:
                data.pop('image')
            # if user.tier.can_generate_link:
            #     data['expiring_link'] = serializers.HyperlinkedIdentityField(view_name='image-detail')
            # data['expiring_link'] = 'link'
        return data
