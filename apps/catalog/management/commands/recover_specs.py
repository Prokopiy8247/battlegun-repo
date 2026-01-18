from django.core.management.base import BaseCommand
from apps.catalog.models import Product, Category
import random

class Command(BaseCommand):
    help = 'Recovers missing specification data based on synthetic logic'

    def handle(self, *args, **kwargs):
        self.stdout.write('Recovering specification data...')

        # Logic from load_synthetic_data.py
        category_defaults = {
            'Pistols': {'power': 'Gas/CO2', 'material': 'Metal, Polymer'},
            'Rifles': {'power': 'AEG', 'material': 'Metal'},
            'Sniper Rifles': {'power': 'Spring', 'material': 'Metal, Polymer'},
            'Shotguns': {'power': 'Spring', 'material': 'Polymer, Metal'},
            'Machine Guns': {'power': 'AEG', 'material': 'Metal'},
        }

        products = Product.objects.all()
        recovered_count = 0

        for product in products:
            cat_name = product.category.name
            defaults = category_defaults.get(cat_name)
            
            if not defaults:
                self.stdout.write(self.style.WARNING(f"Skipping {product.name} (Category {cat_name} unknown)"))
                continue

            # Recover Color
            color = 'Black'
            if 'Tan' in product.name or 'Coyote' in product.name:
                color = 'Tan/Coyote'
            elif 'Olive' in product.name:
                color = 'Olive Drab'
            elif 'Grey' in product.name:
                color = 'Grey'
            elif 'Gold' in product.name:
                color = 'Black/Gold'
            
            # Update fields if they are missing
            updated = False
            
            # We explicitly update the _en fields and the base fields
            # Power Supply
            if not product.power_supply or not product.power_supply_en:
                product.power_supply = defaults['power']
                product.power_supply_en = defaults['power']
                updated = True
            
            # Material
            if not product.material or not product.material_en:
                product.material = defaults['material']
                product.material_en = defaults['material']
                updated = True

            # Color
            if not product.color or not product.color_en:
                product.color = color
                product.color_en = color
                updated = True

            if updated:
                product.save()
                recovered_count += 1
                # self.stdout.write(f"Recovered {product.name}")

        self.stdout.write(self.style.SUCCESS(f'Successfully recovered specs for {recovered_count} products'))
