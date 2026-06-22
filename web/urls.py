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


# Old slug aliases → canonical slug. view_html/view_slash handle the /slug/ vs /slug.html split.
_LEGACY = {
    'contact':  'attestatsiya-rabochikh-mest-s-kompyuterom-pevm',
    'articles': 'attestatsiya-rabochikh-mest-po-professiyam',
    'docs':     'obraztsy-dokumentov-po-attestatsii-rabochikh-mest',
    'contacts': 'kontakty',
}


def _legacy_redirect(request, slug=''):
    """Handles /slug.html: legacy aliases get 301, canonical articles are served."""
    from django.http import HttpResponsePermanentRedirect
    from core.models import Page
    target = _LEGACY.get(slug)
    if target:
        is_cat = Page.objects.filter(category=target, is_published=True).exists()
        url = f'/{target}/' if is_cat else f'/{target}.html'
        return HttpResponsePermanentRedirect(url)
    return views.page_view_html(request, slug=slug)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', robots_txt),
    path('contact-form/', contact_form, name='contact_form'),
    path('', views.page_view, {'slug': 'home'}, name='home'),
    # Joomla URL format: categories at /slug/, articles at /slug.html
    path('<path:slug>.html', _legacy_redirect, name='page_html'),
    path('<slug:slug>/', views.page_view_slash, name='page_slash'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
