from django.core.management.base import BaseCommand
from apps.catalog.models import Product, Category
from deep_translator import GoogleTranslator
import time

class Command(BaseCommand):
    help = 'Automatically translates product content to Polish and Russian'

    def handle(self, *args, **options):
        translator_pl = GoogleTranslator(source='auto', target='pl')
        translator_ru = GoogleTranslator(source='auto', target='ru')

        # Translate Categories
        categories = Category.objects.all()
        self.stdout.write(f"Found {categories.count()} categories to translate...")
        for category in categories:
            self.stdout.write(f"Translating Category: {category.name}")
            try:
                # Update base language if missing (recovery logic inline)
                if not category.name_en:
                     category.name_en = category.name

                if category.name:
                    category.name_pl = translator_pl.translate(category.name)
                    category.name_ru = translator_ru.translate(category.name)
                
                if category.description:
                    category.description_pl = translator_pl.translate(category.description)
                    category.description_ru = translator_ru.translate(category.description)
                
                category.save()
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error translating Category {category.name}: {e}"))

        products = Product.objects.all()
        total = products.count()
        self.stdout.write(f"Found {total} products to translate...")

        for i, product in enumerate(products, 1):
            self.stdout.write(f"[{i}/{total}] Translating: {product.name}")
            
            # Translate to Polish
            try:
                if product.name:
                    product.name_pl = translator_pl.translate(product.name)
                if product.description_short:
                    product.description_short_pl = translator_pl.translate(product.description_short)
                if product.description:
                    product.description_pl = translator_pl.translate(product.description[:4999]) # Limit length safety
                if product.power_supply:
                     product.power_supply_pl = translator_pl.translate(product.power_supply).replace('Wiosna', 'Sprężyna')
                if product.material:
                if product.material:
                     product.material_pl = translator_pl.translate(product.material)
                if product.color:
                     product.color_pl = translator_pl.translate(product.color)
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error translating PL for {product.id}: {e}"))

            # Translate to Russian
            try:
                if product.name:
                    product.name_ru = translator_ru.translate(product.name)
                if product.description_short:
                    product.description_short_ru = translator_ru.translate(product.description_short).replace('кадры в секунду', 'FPS').replace('кадров в секунду', 'FPS')
                if product.description:
                    product.description_ru = translator_ru.translate(product.description[:4999]).replace('кадры в секунду', 'FPS').replace('кадров в секунду', 'FPS')
                if product.power_supply:
                     product.power_supply_ru = translator_ru.translate(product.power_supply).replace('Весна', 'Пружина')
                if product.material:
                if product.material:
                     product.material_ru = translator_ru.translate(product.material)
                if product.color:
                     product.color_ru = translator_ru.translate(product.color)
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error translating RU for {product.id}: {e}"))
            
            product.save()
            # simple rate limiting prevents blocking
            # deep-translator usually handles it but being nice is good
            
        self.stdout.write(self.style.SUCCESS("Successfully translated all products!"))
