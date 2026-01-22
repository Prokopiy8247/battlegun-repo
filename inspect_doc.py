import os
import django
import sys

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.catalog.models import Product

print("Products with brand 'DO&C':")
for p in Product.objects.filter(brand='DO&C'):
    print(f"- {p.name} (SKU: {p.sku})")

print("\nProducts with brand 'E&C':")
print(Product.objects.filter(brand='E&C').count())
