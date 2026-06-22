from django.db import models


class SiteSettings(models.Model):
    question_text = models.CharField('Текст вопроса', max_length=200, default='Остались вопросы?')
    question_link_text = models.CharField('Текст ссылки', max_length=100, default='ЖМИ СЮДА!')
    question_link_url = models.CharField('URL ссылки', max_length=200, default='/contacts/')
    working_hours = models.CharField('Режим работы', max_length=200, default='Пн–Сб 9:00–21:00 · Вс выходной')
    phone = models.CharField('Телефон (основной)', max_length=50, default='+375 29 689-60-66')
    phone_mts = models.CharField('Телефон MTS', max_length=50, default='+375 33 681-60-66')
    email = models.EmailField('Email', default='6896066@tut.by')
    logo_letter = models.CharField('Буква логотипа', max_length=5, default='А')
    logo_name = models.CharField('Название компании', max_length=100, default='АТТЕСТАЦИЯ РМ')
    logo_subtitle = models.CharField('Подпись логотипа', max_length=100, default='МИНСК · БЕЛАРУСЬ')
    cta_text = models.CharField('Текст кнопки CTA', max_length=100, default='Оставить заявку')
    cta_url = models.CharField('URL кнопки CTA', max_length=200, default='/contacts/')
    tagline = models.CharField('Слоган в подвале', max_length=300, default='Качество и оперативность — это наша главная задача!')
    copyright = models.CharField('Копирайт', max_length=300, default='© 2026 Аттестация рабочих мест в Беларуси и Минске. Все права защищены.')

    class Meta:
        verbose_name = 'Настройки сайта'
        verbose_name_plural = 'Настройки сайта'

    def __str__(self):
        return 'Настройки сайта'

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class PartnerLink(models.Model):
    site = models.ForeignKey('SiteSettings', on_delete=models.CASCADE, related_name='partnerlink_set', null=True)
    title = models.CharField('Название', max_length=200)
    url = models.CharField('URL', max_length=500, default='#')
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Партнёр'
        verbose_name_plural = 'Партнёры'
        ordering = ['order']

    def __str__(self):
        return self.title


# ─── NAVIGATION ──────────────────────────────────────────────────────────────

class MenuItem(models.Model):
    """Top-level navigation item. Can be a plain link or open a mega-menu panel."""

    DROPDOWN_NONE = ''
    DROPDOWN_SERVICES = 'services'
    DROPDOWN_DOCS = 'docs'
    DROPDOWN_CHOICES = [
        (DROPDOWN_NONE, 'Обычная ссылка'),
        (DROPDOWN_SERVICES, 'Мегаменю: Услуги'),
        (DROPDOWN_DOCS, 'Мегаменю: Образцы документов'),
    ]

    label = models.CharField('Название пункта', max_length=100)
    url = models.CharField('URL', max_length=500, blank=True,
                           help_text='Оставьте пустым, если пункт открывает мегаменю')
    dropdown = models.CharField('Тип мегаменю', max_length=20,
                                choices=DROPDOWN_CHOICES, blank=True, default='')
    active_key = models.SlugField('Ключ активности', max_length=50, blank=True,
                                  help_text='Slug, по которому подсвечивается активный пункт (напр. «docs», «about»)')
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Пункт меню'
        verbose_name_plural = 'Главное меню'
        ordering = ['order']

    def __str__(self):
        return self.label


class MegaMenuColumn(models.Model):
    """One column inside a mega-menu panel (e.g. «Приказы и протоколы»)."""

    PANEL_CHOICES = [
        ('services', 'Мегаменю: Услуги'),
        ('docs', 'Мегаменю: Образцы документов'),
    ]

    panel = models.CharField('Панель', max_length=20, choices=PANEL_CHOICES, default='docs')
    title = models.CharField('Заголовок колонки', max_length=200)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Колонка мегаменю'
        verbose_name_plural = 'Колонки мегаменю'
        ordering = ['panel', 'order']

    def __str__(self):
        return f'[{self.get_panel_display()}] {self.title}'


class MegaMenuLink(models.Model):
    """One link inside a mega-menu column."""

    column = models.ForeignKey(MegaMenuColumn, on_delete=models.CASCADE,
                               related_name='links', verbose_name='Колонка')
    title = models.CharField('Название', max_length=300)
    description = models.CharField('Короткое описание', max_length=300, blank=True,
                                   help_text='Показывается под названием (только для колонки «Услуги»)')
    url = models.CharField('URL', max_length=500)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Ссылка мегаменю'
        verbose_name_plural = 'Ссылки мегаменю'
        ordering = ['order']

    def __str__(self):
        return self.title


# ─── PAGES ───────────────────────────────────────────────────────────────────

class Page(models.Model):
    title = models.CharField('Заголовок', max_length=300)
    slug = models.CharField('URL (slug)', max_length=500, unique=True,
                            help_text='Часть URL после домена, без слэшей. Например: contacts или obrazets-prikaza-o-provedenii-...')
    active_key = models.SlugField('Ключ меню', max_length=50, blank=True,
                                  help_text='Ключ активности для подсветки пункта меню (напр. «docs», «about»)')
    meta_title = models.CharField('SEO-заголовок', max_length=300, blank=True)
    meta_description = models.TextField('SEO-описание', blank=True)
    content = models.TextField('Контент (HTML)', blank=True)
    is_published = models.BooleanField('Опубликована', default=True)
    updated_at = models.DateTimeField('Изменена', auto_now=True)

    class Meta:
        verbose_name = 'Страница'
        verbose_name_plural = 'Страницы'
        ordering = ['title']

    def __str__(self):
        return f'{self.title} (/{self.slug}/)'

    def get_absolute_url(self):
        return f'/{self.slug}/'
