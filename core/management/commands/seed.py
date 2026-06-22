from django.core.management.base import BaseCommand
from core.models import SiteSettings, PartnerLink, NavItem, ServiceItem, DocGroup, DocLink, Page


class Command(BaseCommand):
    help = 'Seed database with initial content from design'

    def handle(self, *args, **options):
        # SiteSettings
        site, _ = SiteSettings.objects.get_or_create(pk=1)
        self.stdout.write('SiteSettings OK')

        # Partners
        if not PartnerLink.objects.exists():
            partners = [
                ('Форум по охране труда', '#'),
                ('Библиотека по охране труда', '#'),
                ('Разработка СУОТ', '#'),
                ('План проверок по охране труда', '#'),
            ]
            for i, (title, url) in enumerate(partners):
                PartnerLink.objects.create(site=site, title=title, url=url, order=i)
            self.stdout.write('PartnerLinks OK')

        # NavItems
        if not NavItem.objects.exists():
            nav = [
                ('Главная', '/', 'home', '', 0),
                ('О нас', '/about/', 'about', '', 1),
                ('Услуги', '', 'services', 'services', 2),
                ('Образцы документов', '', 'docs', 'docs', 3),
                ('Цены', '/prices/', 'prices', '', 4),
                ('Контакты', '/contacts/', 'contacts', '', 5),
            ]
            for label, url, key, dropdown, order in nav:
                NavItem.objects.create(label=label, url=url, key=key, dropdown=dropdown, order=order)
            self.stdout.write('NavItems OK')

        # Services dropdown
        if not ServiceItem.objects.exists():
            ServiceItem.objects.create(
                title='Аттестация рабочих мест',
                description='Полный комплекс работ «под ключ» по условиям труда',
                url='/', order=0
            )
            ServiceItem.objects.create(
                title='Производственный контроль',
                description='Инструментальные замеры вредных факторов в рамках лабораторного контроля',
                url='/production-control/', order=1
            )
            self.stdout.write('ServiceItems OK')

        # Docs dropdown
        if not DocGroup.objects.exists():
            groups = [
                ('Приказы и протоколы', 0, [
                    ('Приказ о проведении АРМ', '/docs/order-arm/'),
                    ('Перечень факторов для исследования', '/docs/factors-list/'),
                    ('Протокол по тяжести', '/docs/protocol-weight/'),
                    ('Протокол по напряжённости', '/docs/protocol-tension/'),
                    ('Протокол обследования рабочего места', '/docs/protocol-workplace/'),
                    ('Протокол о завершении АРМ', '/docs/protocol-finish/'),
                    ('Приказ об утверждении результатов', '/docs/order-approve/'),
                    ('План мероприятий', '/docs/action-plan/'),
                ]),
                ('Перечни по АРМ', 1, [
                    ('Перечень рабочих мест для аттестации', '/docs/workplaces-list/'),
                    ('Перечень на пенсию', '/docs/pension-list/'),
                    ('Перечень текстильные профессии', '/docs/textile-list/'),
                    ('Перечень на доп. отпуск', '/docs/vacation-list/'),
                    ('Перечень на сокращение рабочего времени', '/docs/hours-list/'),
                    ('Перечень на доплаты', '/docs/bonus-list/'),
                    ('Перечень: условия не подтверждены', '/docs/unconfirmed-list/'),
                    ('Перечень мед. работников', '/docs/medical-list/'),
                ]),
                ('Карты для АРМ', 2, [
                    ('КФРВ по профессиям', '/docs/kfrv/'),
                    ('Правила заполнения КФРВ', '/docs/kfrv-rules/'),
                    ('Карта-фотография в Excel', '/docs/photo-card/'),
                ]),
                ('База знаний по АРМ', 3, [
                    ('Положение о порядке АРМ', '/docs/regulation/'),
                    ('Инструкция по оценке условий труда', '/docs/instruction/'),
                    ('Загрузка АРМ в электронном виде', '/docs/upload/'),
                    ('Вопрос-ответ', '/'),
                ]),
            ]
            for gtitle, gorder, links in groups:
                group = DocGroup.objects.create(title=gtitle, order=gorder)
                for i, (ltitle, lurl) in enumerate(links):
                    DocLink.objects.create(group=group, title=ltitle, url=lurl, order=i)
            self.stdout.write('DocGroups OK')

        # Home page
        if not Page.objects.filter(slug='home').exists():
            Page.objects.create(
                title='Аттестация рабочих мест',
                slug='home',
                nav_key='home',
                meta_title='Аттестация рабочих мест в Минске и Беларуси',
                meta_description='Профессиональная аттестация рабочих мест, производственный контроль, лабораторные замеры. Минск, Беларусь.',
                content='<div style="padding:60px 48px;text-align:center;"><h1 style="font:800 36px/1.2 Manrope,sans-serif;color:#16285a;margin-bottom:16px;">Аттестация рабочих мест</h1><p style="font:500 18px/1.6 Manrope,sans-serif;color:#6a7290;">Главная страница. Контент редактируется в <a href="/admin/" style="color:#ff6a13;font-weight:700;">админке</a>.</p></div>',
                is_published=True,
            )
            self.stdout.write('Home page OK')

        self.stdout.write(self.style.SUCCESS('Seed complete!'))
