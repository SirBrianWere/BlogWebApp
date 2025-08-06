from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.urls import reverse
from .models import Product
from django.contrib.auth.models import User

class ProductSlugTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        
    def test_slug_creation(self):
        product = Product.objects.create(
            name="Test Product",
            description="Test description",
            image="test.jpg",
            author=self.user
        )
        self.assertEqual(product.slug, "test-product")
        
    def test_slug_uniqueness(self):
        product1 = Product.objects.create(
            name="Test Product",
            description="Test description",
            image="test1.jpg",
            author=self.user
        )
        product2 = Product.objects.create(
            name="Test Product",
            description="Test description",
            image="test2.jpg",
            author=self.user
        )
        self.assertEqual(product2.slug, "test-product-1")
        
    def test_slug_urls(self):
        product = Product.objects.create(
            name="Test Product",
            description="Test description",
            image="test.jpg",
            author=self.user
        )
        response = self.client.get(reverse('product_detail', args=[product.slug]))
        self.assertEqual(response.status_code, 302)  # Or 200 if not requiring login