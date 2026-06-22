from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.http import HttpResponse
from core import views
from core.views import contact_form
from core.sitemaps import PageSitemap

sitemaps = {'pages': PageSitemap}


def robots_txt(request):
    content = (
        "User-agent: *\n"
        "Disallow: /admin/\n"
        "Disallow: /media/\n\n"
        "Sitemap: https://attestation.by/sitemap.xml\n"
    )
    return HttpResponse(content, content_type='text/plain')


# Slug aliases: old slug → canonical slug (both redirect to canonical .html URL)
_LEGACY = {
    'contact':  'attestatsiya-rabochikh-mest-s-kompyuterom-pevm',
    'articles': 'attestatsiya-rabochikh-mest-po-professiyam',
    'docs':     'obraztsy-dokumentov-po-attestatsii-rabochikh-mest',
    'contacts': 'kontakty',  # Joomla canonical was /kontakty.html
}


def _legacy_redirect(request, slug=''):
    """Handles /slug.html requests: redirect legacy slugs, serve canonical ones."""
    from django.http import HttpResponsePermanentRedirect
    target = _LEGACY.get(slug)
    if target:
        return HttpResponsePermanentRedirect(f'/{target}.html')
    return views.page_view_html(request, slug=slug)


def _slug_to_html(request, slug=''):
    """301 redirect /slug/ → /slug.html  (canonical format matches old Joomla site)."""
    from django.http import HttpResponsePermanentRedirect
    return HttpResponsePermanentRedirect(f'/{slug}.html')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', robots_txt),
    path('contact-form/', contact_form, name='contact_form'),
    path('', views.page_view, {'slug': 'home'}, name='home'),
    # Canonical URL format: /slug.html  (matches old Joomla site)
    path('<path:slug>.html', _legacy_redirect, name='page_html'),
    # Legacy /slug/ → 301 → /slug.html
    path('<path:slug>/', _slug_to_html, name='page'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
