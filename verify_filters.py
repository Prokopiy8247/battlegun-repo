import os
import django
import sys

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.catalog.models import Product

print("Current Power Supplies in DB:")
ps = list(Product.objects.exclude(power_supply__isnull=True).values_list('power_supply', flat=True).distinct())
print(ps)

print("\nCurrent Manufacturers in DB:")
brands = list(Product.objects.exclude(brand__isnull=True).values_list('brand', flat=True).distinct())
print(brands)
