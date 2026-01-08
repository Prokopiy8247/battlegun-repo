from django.core.management.base import BaseCommand
from apps.catalog.models import Product
import random

class Command(BaseCommand):
    help = 'Updates product descriptions based on their specifications'

    def handle(self, *args, **kwargs):
        products = Product.objects.all()
        count = 0
        
        templates = [
            "Experience superior performance with the {name} by {brand}. This {power_supply} powered replica is built from high-quality {material}, ensuring durability on the field. With a muzzle velocity of {fps} FPS, it delivers precision and power for every shot. Weighing in at {weight}g, it offers a realistic handling experience.",
            
            "Dominate the battlefield with the {brand} {name}. Engineered with {material} construction, this {power_supply} airsoft gun combines reliability with a solid feel ({weight}g). It shoots at an impressive {fps} FPS, making it an excellent choice for competitive play.",
            
            "The {name} represents the quality craftsmanship of {brand}. Featuring a robust {material} body and {power_supply} operation, this replica stands out with its {fps} FPS performance. At {weight}g, it provides the substantial feel that enthusiasts demand.",
            
            "Take your game to the next level with the {name}. {brand} has designed this {power_supply} model using {material} for maximum resilience. Clocking in at {fps} FPS and weighing {weight}g, it's the perfect balance of power and realism.",
            
            "Discover the precision of the {name} from {brand}. This {power_supply} replica features {material} build quality and a weight of {weight}g for authentic handling. With a consistent output of {fps} FPS, you'll have the edge in any skirmish."
        ]

        for product in products:
            # Prepare context, handling None values gracefully
            context = {
                'brand': product.brand or "Unknown Brand",
                'name': product.name,
                'power_supply': product.power_supply or "standard",
                'material': product.material or "composite materials",
                'fps': product.muzzle_velocity_fps or "standard",
                'weight': product.weight_g or "standard"
            }
            
            # Select a random template
            new_description = random.choice(templates).format(**context)
            
            product.description = new_description
            product.save()
            count += 1
            
        self.stdout.write(self.style.SUCCESS(f'Successfully updated descriptions for {count} products'))
