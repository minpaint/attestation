from .models import SiteSettings, MenuItem, MegaMenuColumn


def site_settings(request):
    site = SiteSettings.get()
    nav_items = MenuItem.objects.all()

    # Mega menu panels (prefetch links for each column)
    mega_services = (MegaMenuColumn.objects
                     .filter(panel='services')
                     .prefetch_related('links')
                     .order_by('order'))
    mega_docs = (MegaMenuColumn.objects
                 .filter(panel='docs')
                 .prefetch_related('links')
                 .order_by('order'))

    # Active nav key from URL path
    path = request.path.rstrip('/')
    active_key = ''
    static_map = {
        '': 'home',
        '/about': 'about',
        '/contacts': 'contacts',
    }
    if path in static_map:
        active_key = static_map[path]
    elif path.startswith('/attestatsiya-rabochikh-mest-po-usloviyam-truda-v-minske'):
        active_key = 'prices'
    elif path.startswith('/proizvodstvennyj-kontrol'):
        active_key = 'services'
    else:
        # Match against MegaMenuLink URLs → mark parent panel active
        for col in mega_docs:
            for link in col.links.all():
                if link.url.rstrip('/') == path:
                    active_key = 'docs'
                    break
            if active_key:
                break

    return {
        'site': site,
        'nav_items': nav_items,
        'mega_services': mega_services,
        'mega_docs': mega_docs,
        'active_key': active_key,
    }
