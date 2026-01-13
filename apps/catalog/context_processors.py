from django.core.cache import cache
from .models import Category

def categories(request):
    def get_categories():
        return list(Category.objects.filter(is_active=True).order_by('name'))
    
    categories_list = cache.get_or_set('categories_list', get_categories, 3600)
    return {
        'categories': categories_list
    }
