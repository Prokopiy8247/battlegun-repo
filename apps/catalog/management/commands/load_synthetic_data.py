from django.core.management.base import BaseCommand
from apps.catalog.models import Category, Product
from decimal import Decimal
import random

class Command(BaseCommand):
    help = 'Loads synthetic airsoft data into the database'

    def handle(self, *args, **kwargs):
        self.stdout.write('Loading synthetic data...')

        # Categories
        categories_data = [
            {'name': 'Pistols', 'slug': 'pistols', 'defaults': {'power': 'Gas/CO2', 'weight': 800, 'fps': 300, 'material': 'Metal, Polymer'}},
            {'name': 'Rifles', 'slug': 'rifles', 'defaults': {'power': 'AEG', 'weight': 2500, 'fps': 380, 'material': 'Metal'}},
            {'name': 'Sniper Rifles', 'slug': 'sniper-rifles', 'defaults': {'power': 'Spring', 'weight': 3000, 'fps': 450, 'material': 'Metal, Polymer'}},
            {'name': 'Shotguns', 'slug': 'shotguns', 'defaults': {'power': 'Spring', 'weight': 2000, 'fps': 300, 'material': 'Polymer, Metal'}},
            {'name': 'Machine Guns', 'slug': 'machine-guns', 'defaults': {'power': 'AEG', 'weight': 5000, 'fps': 400, 'material': 'Metal'}},
        ]

        categories = {}
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults={'name': cat_data['name']}
            )
            categories[cat_data['name']] = category
            if created:
                self.stdout.write(f'Created category: {category.name}')

        # Products Data
        products_data = {
            'Pistols': [
                {'name': 'East Crane EC-3101 airsoft pistol', 'price': '96.64', 'brand': 'E&C'},
                {'name': 'RAVEN EU17 pistol replica - black', 'price': '117.67', 'brand': 'NUPROL'},
                {'name': 'East Crane EC-1202 airsoft pistol Black', 'price': '109.66', 'brand': 'E&C'},
                {'name': 'East Crane airsoft pistol EC-2102 Black', 'price': '138.20', 'brand': 'E&C'},
                {'name': 'SR92A1 Pistol Replica', 'price': '145.71', 'brand': 'SRC'},
                {'name': 'East Crane EC-1201 Tan airsoft pistol', 'price': '110.16', 'brand': 'E&C'},
                {'name': 'GBB Glock 19X Green Gas replica pistol - Coyote', 'price': '205.30', 'brand': 'UMAREX'},
                {'name': 'East Crane EC-2101 airsoft pistol', 'price': '109.66', 'brand': 'E&C'},
                {'name': 'East Crane EC-1203 airsoft pistol Black and gold', 'price': '117.42', 'brand': 'E&C'},
            ],
            'Rifles': [
                {'name': 'Specna Arms SA-F10 FLEX™ GATE X-ASR airsoft Carbine', 'price': '149.46', 'brand': 'SPECNA ARMS'},
                {'name': 'Specna Arms SA-F11 FLEX™ GATE X-ASR airsoft Carbine Black', 'price': '149.46', 'brand': 'SPECNA ARMS'},
                {'name': 'Arcturus Sword® MOD1 Carbine 13.5" AEG LITE FE™ airsoft Carbine', 'price': '225.32', 'brand': 'ARCTURUS'},
                {'name': 'airsoft Arcturus LWT MK-III Carbine 12" SPORT AEG SE® Black', 'price': '162.73', 'brand': 'ARCTURUS'},
                {'name': 'Assault rifle airsoft Fabryka Broni Radom wz.96C Beryl with Coyote Brown cover', 'price': '420.61', 'brand': 'MARKA NIEZDEFINIOWANA'},
                {'name': 'Assault rifle airsoft Fabryka Broni Radom wz.96C Beryl with cover Grey', 'price': '701.01', 'brand': 'MARKA NIEZDEFINIOWANA'},
                {'name': '#Starter Pack: Specna Arms SA-F11 FLEX™ GATE X-ASR airsoft Carbine Black', 'price': '125.18', 'brand': 'SPECNA ARMS'},
                {'name': 'Arcturus LWT MK-I CQB 10" AEG SPORT SE™ airsoft Carbine Black', 'price': '162.73', 'brand': 'ARCTURUS'},
                {'name': 'Airsoft assault rifle Cyma CM028', 'price': '122.68', 'brand': 'CYMA'},
            ],
            'Sniper Rifles': [
                {'name': 'CM703 Sniper Rifle Replica', 'price': '120.17', 'brand': 'CYMA'},
                {'name': 'Selective airsoft rifle - SNR25', 'price': '375.54', 'brand': 'A&K'},
                {'name': 'SA-S02 CORE™ Sniper Rifle Replica with Scope and Bipod - Black', 'price': '185.27', 'brand': 'SPECNA ARMS'},
                {'name': 'CM057A sniper rifle replica', 'price': '237.84', 'brand': 'CYMA'},
                {'name': 'CM702 sniper rifle replica', 'price': '117.67', 'brand': 'CYMA'},
                {'name': 'Specna Arms SA-S14 EDGE™ sniper airsoft rifle Black', 'price': '202.79', 'brand': 'SPECNA ARMS'},
                {'name': 'CM701C Sniper Rifle Replica', 'price': '117.67', 'brand': 'CYMA'},
                {'name': 'SA-S02 CORE™ Sniper Rifle Replica - Olive Drab', 'price': '120.17', 'brand': 'SPECNA ARMS'},
                {'name': 'SA-S03 CORE™ Sniper Rifle Replica with Scope and Bipod - Black', 'price': '212.81', 'brand': 'SPECNA ARMS'},
            ],
            'Shotguns': [
                {'name': 'CM350 Long Shotgun Replica', 'price': '60.08', 'brand': 'CYMA'},
                {'name': 'Specna Arms SA-VGS5 VAPOR™ airsoft shotgun Black', 'price': '158.98', 'brand': 'SPECNA ARMS'},
                {'name': 'CM351 shotairsoft gun', 'price': '52.57', 'brand': 'CYMA'},
                {'name': 'Specna Arms SA-VGS3 VAPOR™ airsoft Rifle Black', 'price': '158.98', 'brand': 'SPECNA ARMS'},
                {'name': 'Specna Arms SA-VGS7 VAPOR™ airsoft Rifle Black', 'price': '209.05', 'brand': 'SPECNA ARMS'},
                {'name': 'CM360 Shotgun Replica', 'price': '65.09', 'brand': 'CYMA'},
                {'name': 'Replica Double Bell 007 shotgun', 'price': '235.34', 'brand': 'DOUBLE BELL'},
                {'name': 'Genesis Arms Gen-12 Kestrel ETU Grey airsoft Double Bell TTI Shotgun', 'price': '390.56', 'brand': 'DOUBLE BELL'},
                {'name': 'Specna Arms SA-VGS13 VAPOR™ Real Wood airsoft Shotgun', 'price': '200.29', 'brand': 'SPECNA ARMS'},
            ],
            'Machine Guns': [
                {'name': 'SA-249 MK2 CORE™ machine gun replica - black', 'price': '425.61', 'brand': 'SPECNA ARMS'},
                {'name': 'SA-249 MK1 CORE™ machine gun replica - black', 'price': '425.61', 'brand': 'SPECNA ARMS'},
                {'name': 'SA-249 PARA CORE™ machine gun replica - black', 'price': '425.61', 'brand': 'SPECNA ARMS'},
                {'name': '6669 machine gun replica', 'price': '363.02', 'brand': 'GOLDEN EAGLE'},
                {'name': '6671 machine gun replica', 'price': '363.02', 'brand': 'GOLDEN EAGLE'},
                {'name': 'SA-249 PARA CORE™ machine gun replica - tan', 'price': '425.61', 'brand': 'SPECNA ARMS'},
            ]
        }

        for cat_name, products in products_data.items():
            category = categories[cat_name]
            cat_defaults = next(item['defaults'] for item in categories_data if item['name'] == cat_name)
            
            for prod_data in products:
                # Add some randomness to defaults to make it look realistic
                weight = cat_defaults['weight'] + random.randint(-100, 100)
                fps = cat_defaults['fps'] + random.randint(-20, 20)
                
                # Determine color from name if possible, else default
                color = 'Black'
                if 'Tan' in prod_data['name'] or 'Coyote' in prod_data['name']:
                    color = 'Tan/Coyote'
                elif 'Olive' in prod_data['name']:
                    color = 'Olive Drab'
                elif 'Grey' in prod_data['name']:
                    color = 'Grey'
                elif 'Gold' in prod_data['name']:
                    color = 'Black/Gold'

                product, created = Product.objects.get_or_create(
                    name=prod_data['name'],
                    defaults={
                        'sku': f"{prod_data['brand'][:3].upper()}-{random.randint(1000, 9999)}",
                        'description_short': f"High quality {cat_name.lower()} from {prod_data['brand']}.",
                        'description': f"Full description for {prod_data['name']}. Features robust construction and reliable performance.",
                        'price': Decimal(prod_data['price']),
                        'category': category,
                        'stock': random.randint(1, 20),
                        'is_active': True,
                        
                        # Airsoft details
                        'brand': prod_data['brand'],
                        'color': color,
                        'weight_g': weight,
                        'power_supply': cat_defaults['power'],
                        'material': cat_defaults['material'],
                        'muzzle_velocity_fps': fps,
                    }
                )
                
                if created:
                    self.stdout.write(f"Created product: {product.name}")
                else:
                    self.stdout.write(f"Product exists: {product.name}")

        self.stdout.write(self.style.SUCCESS('Successfully loaded synthetic data'))
