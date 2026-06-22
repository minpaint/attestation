from django.contrib import admin
from django.utils.html import format_html
from ckeditor.widgets import CKEditorWidget
from .models import SiteSettings, PartnerLink, MenuItem, MegaMenuColumn, MegaMenuLink, Page


# ─── SITE SETTINGS ───────────────────────────────────────────────────────────

class PartnerLinkInline(admin.TabularInline):
    model = PartnerLink
    extra = 1
    fields = ['title', 'url', 'order']


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Верхняя строка', {
            'fields': ['question_text', 'question_link_text', 'question_link_url', 'working_hours'],
        }),
        ('Контакты', {
            'fields': ['phone', 'phone_mts', 'email'],
        }),
        ('Логотип', {
            'fields': ['logo_letter', 'logo_name', 'logo_subtitle'],
        }),
        ('Кнопка «Оставить заявку»', {
            'fields': ['cta_text', 'cta_url'],
        }),
        ('Подвал', {
            'fields': ['tagline', 'copyright'],
        }),
    ]
    inlines = [PartnerLinkInline]

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        # Redirect directly to the single object
        obj = SiteSettings.get()
        from django.http import HttpResponseRedirect
        from django.urls import reverse
        return HttpResponseRedirect(
            reverse('admin:core_sitesettings_change', args=[obj.pk])
        )


# ─── NAVIGATION ──────────────────────────────────────────────────────────────

class MegaMenuLinkInline(admin.TabularInline):
    model = MegaMenuLink
    extra = 2
    fields = ['title', 'description', 'url', 'order']


@admin.register(MegaMenuColumn)
class MegaMenuColumnAdmin(admin.ModelAdmin):
    list_display = ['panel', 'title', 'link_count', 'order']
    list_display_links = ['title']
    list_editable = ['order']
    list_filter = ['panel']
    ordering = ['panel', 'order']
    inlines = [MegaMenuLinkInline]

    @admin.display(description='Ссылок')
    def link_count(self, obj):
        return obj.links.count()


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'label', 'url_display', 'dropdown', 'active_key']
    list_display_links = ['label']
    list_editable = ['order']
    ordering = ['order']
    fields = ['label', 'url', 'dropdown', 'active_key', 'order']

    @admin.display(description='URL / Мегаменю')
    def url_display(self, obj):
        if obj.dropdown:
            panel_name = dict(MenuItem.DROPDOWN_CHOICES).get(obj.dropdown, obj.dropdown)
            return format_html('<span style="color:#888;">▼ {}</span>', panel_name)
        return format_html('<a href="{}" target="_blank">{}</a>', obj.url, obj.url) if obj.url else '—'


# ─── PAGES ───────────────────────────────────────────────────────────────────

class PageAdminForm(admin.ModelAdmin.__bases__[0] if False else object):
    pass

import django.forms as forms

class PageForm(forms.ModelForm):
    content = forms.CharField(
        label='Контент',
        widget=CKEditorWidget(),
        required=False,
    )

    class Meta:
        model = Page
        fields = '__all__'


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    form = PageForm
    list_display = ['title', 'slug_link', 'active_key', 'is_published', 'updated_at']
    list_display_links = ['title']
    list_filter = ['is_published', 'active_key']
    search_fields = ['title', 'slug', 'meta_title']
    readonly_fields = ['updated_at', 'slug_preview']
    fieldsets = [
        (None, {
            'fields': ['title', 'slug', 'slug_preview', 'active_key', 'is_published'],
        }),
        ('SEO', {
            'fields': ['meta_title', 'meta_description'],
            'classes': ['collapse'],
            'description': 'Заголовок и описание для поисковых систем',
        }),
        ('Контент', {
            'fields': ['content'],
        }),
        ('Служебное', {
            'fields': ['updated_at'],
            'classes': ['collapse'],
        }),
    ]

    @admin.display(description='URL')
    def slug_link(self, obj):
        url = f'/{obj.slug}/'
        return format_html('<a href="{}" target="_blank">/{}/</a>', url, obj.slug[:60])

    @admin.display(description='Адрес страницы')
    def slug_preview(self, obj):
        if obj.slug:
            url = f'/{obj.slug}/'
            return format_html(
                '<a href="{url}" target="_blank" style="font-family:monospace;">{url}</a>',
                url=url,
            )
        return '—'
