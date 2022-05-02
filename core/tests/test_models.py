from email.policy import EmailPolicy
from django.test import TestCase
from django.contrib.auth import get_user_model


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


