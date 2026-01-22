import os
import django
import sys
from django.conf import settings

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.template.loader import render_to_string

try:
    print("Rendering template...")
    context = {
        'products': [],
        'all_power_supplies': ['Gas', 'AEG'],
        'all_manufacturers': ['Specna'],
        'selected_power_supplies': [],
        'selected_manufacturers': [],
    }
    render_to_string('catalog/product_list.html', context)
    print("Render successful.")
except Exception as e:
    print("Render failed:")
    print(e)
    # Print traceback
    import traceback
    traceback.print_exc()
