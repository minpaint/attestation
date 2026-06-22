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


# Old Joomla aliases that differed from article slugs — 301 redirects
_LEGACY = {
    'contact': 'attestatsiya-rabochikh-mest-s-kompyuterom-pevm',
}


def _legacy_redirect(request, slug=''):
    target = _LEGACY.get(slug)
    if target:
        from django.http import HttpResponsePermanentRedirect
        return HttpResponsePermanentRedirect(f'/{target}/')
    return views.page_view_html(request, slug=slug)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', robots_txt),
    path('contact-form/', contact_form, name='contact_form'),
    path('', views.page_view, {'slug': 'home'}, name='home'),
    # Old Joomla URLs ending in .html — strip suffix and serve same page (or redirect)
    path('<path:slug>.html', _legacy_redirect, name='page_html'),
    path('<path:slug>/', views.page_view, name='page'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
