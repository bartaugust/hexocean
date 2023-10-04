from django.test import TestCase, override_settings
from django.core.management import call_command
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from .models import User, UserTier, UploadedImage

TEST_DIR = 'test_media'


# Create your tests here.
class UserTierTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command('prepare_database')
        cls.tiers = UserTier.objects.all()
        cls.users = {}
        for tier in cls.tiers:
            cls.users[tier.name] = User.objects.create_user(
                username=f'test_{tier.name}',
                email=f'test_{tier.name}@email.com',
                password='Test123.',
                tier=tier,
            )

        image_file = '../media/test_images/bird.jpg'
        for tier_name, user in cls.users.items():
            UploadedImage.objects.create(
                image=image_file,
                user=user,

            )

    def test_basic_tiers(self):
        assert len(self.tiers) == 3
        for tier in self.tiers:
            if tier.name == 'Basic':
                assert tier.is_link_present is False
                assert tier.can_generate_link is False
                self.assertListEqual(tier.thumbnail_sizes, [200])
            elif tier.name == 'Premium':
                assert tier.is_link_present is True
                assert tier.can_generate_link is False
                self.assertListEqual(tier.thumbnail_sizes, [200, 400])
            elif tier.name == 'Enterprise':
                assert tier.is_link_present is True
                assert tier.can_generate_link is True
                self.assertListEqual(tier.thumbnail_sizes, [200, 400])
            else:
                assert False

    def test_create_tier(self):
        UserTier.objects.create(
            name='new_tier',
            thumbnail_sizes=[200, 400, 500],
            is_link_present=False,
            can_generate_link=True,
        )


class UserApiTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        call_command('prepare_database')
        cls.tiers = UserTier.objects.all()
        cls.users = {}
        for tier in cls.tiers:
            cls.users[tier.name] = User.objects.create_user(
                username=f'test_{tier.name}',
                email=f'test_{tier.name}@email.com',
                password='Test123.',
                tier=tier,
            )

        cls.image_file = '../media/test_images/bird.jpg'
        for tier_name, user in cls.users.items():
            UploadedImage.objects.create(
                image=cls.image_file,
                user=user,

            )

    def test_images_list_authentication(self):
        url = reverse('images-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        for tier_name, user in self.users.items():
            self.client.login(username=user.username, password='Test123.')
            response = self.client.get(url, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.client.logout()
