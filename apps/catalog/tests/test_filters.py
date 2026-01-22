from django.test import TestCase, Client
from django.urls import reverse
from apps.catalog.models import Product, Category

class ProductFilterTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name='Rifles', slug='rifles')
        
        # Create products with different attributes
        self.p1 = Product.objects.create(
            name='Gun 1', slug='gun-1', sku='G1', price=100, category=self.category,
            power_supply='AEG', brand='CYMA'
        )
        self.p2 = Product.objects.create(
            name='Gun 2', slug='gun-2', sku='G2', price=100, category=self.category,
            power_supply='Gas', brand='SPECNA ARMS'
        )
        self.p3 = Product.objects.create(
            name='Gun 3', slug='gun-3', sku='G3', price=100, category=self.category,
            power_supply='Spring', brand='CYMA'
        )

    def test_filter_by_power_supply(self):
        response = self.client.get(reverse('product_list'), {'power_supply': 'AEG'})
        self.assertContains(response, self.p1.name)
        self.assertNotContains(response, self.p2.name)
        self.assertNotContains(response, self.p3.name)

        # Test multiple
        response = self.client.get(reverse('product_list'), {'power_supply': ['AEG', 'Spring']})
        self.assertContains(response, self.p1.name)
        self.assertNotContains(response, self.p2.name)
        self.assertContains(response, self.p3.name)

    def test_filter_by_brand(self):
        response = self.client.get(reverse('product_list'), {'manufacturer': 'CYMA'})
        self.assertContains(response, self.p1.name)
        self.assertContains(response, self.p3.name)
        self.assertNotContains(response, self.p2.name)

    def test_combined_filters(self):
        # Brand CYMA AND Power Supply AEG -> p1 only
        response = self.client.get(reverse('product_list'), {'manufacturer': 'CYMA', 'power_supply': 'AEG'})
        self.assertContains(response, self.p1.name)
        self.assertNotContains(response, self.p2.name)
        self.assertNotContains(response, self.p3.name)
