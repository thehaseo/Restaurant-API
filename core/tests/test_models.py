from django.test import TestCase
from django.contrib.auth import get_user_model

from . import models


def sample_user(email='test@gmail.com', password='password123'):
    return get_user_model().objects.create_user(email, password)


class ModelTest(TestCase):

    def test_create_user_with_email_successful(self):
        """ test creating new user with email as username """
        email = 'test@gmail.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email = email,
            password = password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """test normalized email for new user"""
        email = 'test@gmAil.com'
        user = get_user_model().objects.create_user(
            email=email,
            password='testpass123'
        )

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'testpass123')

    def test_create_new_superuser(self):
        email = 'test@gmail.com'
        password = 'testpass123'
        user = get_user_model().objects.create_superuser(
            email = email,
            password = password
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """Test __str__ method in tag model"""
        tag = models.Tag.objects.create(user=sample_user(), name='Chicken')

        self.assertEqual(str(tag), tag.name)

