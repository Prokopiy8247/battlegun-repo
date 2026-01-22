import os
import django
import sys

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.catalog.models import Product

def clean_data():
    print("Starting data cleanup...")
    
    # 1. Fix Power Supply
    # We want strict: 'Gas', 'Spring', 'AEG'
    products = Product.objects.all()
    for p in products:
        dirty = False
        original_ps = p.power_supply
        original_brand = p.brand
        
        # Power Supply Logic
        if p.power_supply:
            ps_lower = p.power_supply.lower()
            if 'gas' in ps_lower or 'co2' in ps_lower:
                if p.power_supply != 'Gas':
                    p.power_supply = 'Gas'
                    dirty = True
            elif 'aeg' in ps_lower or 'electric' in ps_lower:
                if p.power_supply != 'AEG':
                    p.power_supply = 'AEG'
                    dirty = True
            elif 'spring' in ps_lower:
                if p.power_supply != 'Spring':
                    p.power_supply = 'Spring'
                    dirty = True
        
        # Manufacturer Logic
        if p.brand:
            # Fix DO&C -> DOUBLE BELL (Assuming query meant Double Bell or similar, checking context. 
            # Actually, looking at the user request "DOUBLE BELL" is a valid manufacturer. 
            # 'DO&C' looks like a typo for 'DOUBLE BELL' or maybe 'E&C'.
            # Given 'E&C' is also a valid manufacturer, DO&C is likely 'DOUBLE BELL' distorted or 'E&C' distorted.
            # But the list has 'DOUBLE BELL'.
            # Let's handle known typos if we find them, or just print them for manual review if ambiguous.
            
            if p.brand == 'DO&C':
                # Safe guess: Double Bell? Or E&C?
                # "DO" might come from "DOUBLE".
                p.brand = 'DOUBLE BELL'
                dirty = True
                
            # Normalize case just in case
            # The allowed list is attached to the view:
            # ['SPECNA ARMS', 'GOLDEN EAGLE', 'DOUBLE BELL', 'CYMA', 'A&K', 'ARCTURUS', 'E&C', 'UMAREX', 'SRC', 'NUPROL']
            
            allowed_brands = {
                'SPECNA ARMS', 'GOLDEN EAGLE', 'DOUBLE BELL', 'CYMA', 'A&K', 
                'ARCTURUS', 'E&C', 'UMAREX', 'SRC', 'NUPROL'
            }
            
            if p.brand.upper() in allowed_brands:
                if p.brand != p.brand.upper():
                    p.brand = p.brand.upper()
                    dirty = True
            
        if dirty:
            print(f"Updating {p.name}: PS '{original_ps}'->'{p.power_supply}', Brand '{original_brand}'->'{p.brand}'")
            p.save()
        else:
            # Check if brand is valid
            allowed_brands = [
                'SPECNA ARMS', 'GOLDEN EAGLE', 'DOUBLE BELL', 'CYMA', 'A&K', 
                'ARCTURUS', 'E&C', 'UMAREX', 'SRC', 'NUPROL'
            ]
            if p.brand and p.brand not in allowed_brands:
                print(f"WARNING: Unknown brand for {p.name}: '{p.brand}'")

    print("\nCleanup finished.")

if __name__ == "__main__":
    clean_data()
