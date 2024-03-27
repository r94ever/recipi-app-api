from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase

from core import models


class ModelTests(TestCase):
    def test_create_user_with_email_successful(self):
        email = 'test@example.com'
        password = 'test_pass_123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        sample_emails = [
            ['Test1@EXample.com', 'Test1@example.com'],
            ['TEST2@EXample.COm', 'TEST2@example.com'],
            ['TEST3@EXAMPle.COM', 'TEST3@example.com'],
            ['TEst4@EXAMPle.CoM', 'TEst4@example.com'],
        ]
        password = 'test_pass_123'

        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(
                email=email,
                password=password
            )
            self.assertEqual(user.email, expected)

    def test_user_without_email_raise_error(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_superuser(self):
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_recipe(self):
        """Test creating recipe successful"""
        user = get_user_model().objects.create_user(
            email='test@example.com',
            password='test_pass_123'
        )
        recipe = models.Recipe.objects.create(
            user=user,
            title='Test Recipe',
            time_minutes=5,
            price=Decimal('5.50'),
            description='Test Description'
        )
        self.assertEqual(str(recipe), recipe.title)
