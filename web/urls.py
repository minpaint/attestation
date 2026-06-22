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


urlpatterns = [
    path('admin/', admin.site.urls),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', robots_txt),
    path('contact-form/', contact_form, name='contact_form'),
    path('', views.page_view, {'slug': 'home'}, name='home'),
    # Old Joomla URLs ending in .html — strip suffix and serve same page
    path('<path:slug>.html', views.page_view_html, name='page_html'),
    path('<path:slug>/', views.page_view, name='page'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
