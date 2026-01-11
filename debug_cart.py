import os
import django
from django.conf import settings
from django.template import engines
from django.test import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware

# Setup Django (already setup in shell, but good for standalone)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

def debug_render():
    try:
        from django.template import loader, RequestContext
        
        factory = RequestFactory()
        request = factory.get('/')
        
        # Add session
        middleware = SessionMiddleware(lambda x: None)
        middleware.process_request(request)
        request.session.save()
        
        # Render base.html
        t = loader.get_template('base.html')
        
        # Manually run context processors to see if they crash or work
        from apps.cart.context_processors import cart
        print("Context Processor Result:", cart(request))
        
        # Render
        # We need to simulate how Django renders views
        # RequestContext will load context processors defined in settings
        context = {} 
        # Note: In newer Django, we might need to pass request to render
        rendered = t.render(context, request)
        
        if "{{ cart.total_items }}" in rendered:
            print("FAILURE: Found literal {{ cart.total_items }} in output.")
        else:
            print("SUCCESS: Tags were processed.")
            # Print a snippet
            import re
            match = re.search(r'header-cart-count.*?</span>', rendered, re.DOTALL)
            if match:
                print("Snippet:", match.group(0))
            else:
                print("Snippet not found")

    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

debug_render()
