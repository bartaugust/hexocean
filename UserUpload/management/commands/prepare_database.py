from django.core.management.base import BaseCommand

from UserUpload.models import UserTier


class Command(BaseCommand):
    def handle(self, *args, **options):
        UserTier.objects.create(
            name='Basic',
            thumbnail_sizes=[200],
        )
        UserTier.objects.create(
            name='Premium',
            thumbnail_sizes=[200, 400],
            is_link_present=True,
        )
        UserTier.objects.create(
            name='Enterprise',
            thumbnail_sizes=[200, 400],
            is_link_present=True,
            can_generate_link=True,
        )
