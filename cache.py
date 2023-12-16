# Using Cache, it has two methods, get('key_name') and set('key':'value', duration)
from django.core.cache import cache

def setting_page_cache(request):
    data = request.data.get('cacheMetaData')  # Assuming 'cacheMetaData' is a key in request.data
    cache.set('data', data, 600 * 15)  # Save it for 15 minutes

def get_page_cache(request):
    data = cache.get('data')
    return data

