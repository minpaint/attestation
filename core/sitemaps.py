# -*- coding: utf-8 -*-
from django.contrib.sitemaps import Sitemap
from .models import Page


class PageSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.7
    protocol = 'https'

    def items(self):
        return Page.objects.filter(is_published=True).order_by('slug')

    def location(self, obj):
        if obj.slug == 'home':
            return '/'
        # Category pages at /slug/, articles at /slug.html — mirrors Joomla structure
        from .models import Page
        if Page.objects.filter(category=obj.slug, is_published=True).exists():
            return f'/{obj.slug}/'
        return f'/{obj.slug}.html'

    def lastmod(self, obj):
        return obj.updated_at

    def priority_for(self, obj):
        if obj.slug == 'home':
            return 1.0
        if obj.slug in ('about', 'contacts', 'docs', 'articles'):
            return 0.8
        return 0.7
