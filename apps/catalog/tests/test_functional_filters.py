from django.test import TestCase, Client
from django.urls import reverse
from apps.catalog.models import Product, Category

class ProductFilterTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Rifles", slug="rifles")
        
        # Create Products
        self.p1 = Product.objects.create(
            name="Specna Arms SA-E01",
            slug="sa-e01",
            sku="SA001",
            description="Good rifle",
            price=100.00,
            category=self.category,
            power_supply="AEG",
            brand="SPECNA ARMS"
        )
        
        self.p2 = Product.objects.create(
            name="Golden Eagle Gas Shotgun",
            slug="ge-gas",
            sku="GE001",
            description="Boom",
            price=150.00,
            category=self.category,
            power_supply="Gas",
            brand="GOLDEN EAGLE"
        )
        
        self.p3 = Product.objects.create(
            name="Specna Arms Gas Pistol",
            slug="sa-gas",
            sku="SA002",
            description="Pew pew",
            price=50.00,
            category=self.category,
            power_supply="Gas",
            brand="SPECNA ARMS"
        )

        self.url = reverse('product_list')

    def test_filter_by_power_supply(self):
        response = self.client.get(self.url, {'power_supply': 'Gas'})
        self.assertEqual(response.status_code, 200)
        products = list(response.context['products'])
        self.assertIn(self.p2, products)
        self.assertIn(self.p3, products)
        self.assertNotIn(self.p1, products)

    def test_filter_by_manufacturer(self):
        response = self.client.get(self.url, {'manufacturer': 'SPECNA ARMS'})
        self.assertEqual(response.status_code, 200)
        products = list(response.context['products'])
        self.assertIn(self.p1, products)
        self.assertIn(self.p3, products)
        self.assertNotIn(self.p2, products)
        
    def test_filter_combined(self):
        response = self.client.get(self.url, {
            'power_supply': 'Gas',
            'manufacturer': 'SPECNA ARMS'
        })
        self.assertEqual(response.status_code, 200)
        products = list(response.context['products'])
        self.assertIn(self.p3, products)
        self.assertNotIn(self.p1, products)
        self.assertNotIn(self.p2, products)

    def test_filter_multiple_values(self):
        # Filter for Gas OR AEG
        response = self.client.get(self.url, {'power_supply': ['Gas', 'AEG']})
        products = list(response.context['products'])
        self.assertIn(self.p1, products)
        self.assertIn(self.p2, products)
        self.assertIn(self.p3, products)
