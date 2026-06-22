"""
Import all pages from the design folder into the database.
Strips dc-import, x-dc, sc-if, helmet tags and replaces .dc.html hrefs with Django URLs.
"""
import re
from django.core.management.base import BaseCommand
from core.models import Page

PAGES = {
    'home': {
        'title': 'Аттестация рабочих мест',
        'active_key': 'home',
        'meta_title': 'Аттестация рабочих мест в Минске и Беларуси',
        'meta_description': 'Проведение аттестации рабочих мест «под ключ». Собственная аккредитованная лаборатория. Минск и вся Беларусь.',
        'file': 'Главная.dc.html',
    },
    'about': {
        'title': 'О компании',
        'active_key': 'about',
        'meta_title': 'О компании — аттестация рабочих мест',
        'meta_description': 'ООО «Полitekс-оптималь» — с 2000 года проводим аттестации рабочих мест. Собственная лаборатория, более 1200 аттестаций.',
        'file': 'О нас.dc.html',
    },
    # Real URL from Joomla DB (alias id=130)
    'attestatsiya-rabochikh-mest-po-usloviyam-truda-v-minske-tseny-stoimost-odnogo-rabochego-mesta': {
        'title': 'Стоимость аттестации',
        'active_key': 'prices',
        'meta_title': 'Цены на аттестацию рабочих мест в Минске',
        'meta_description': 'Стоимость аттестации рабочих мест. Гибкие цены, эффект объёма, НДС включён в стоимость.',
        'file': 'Цены.dc.html',
    },
    'contacts': {
        'title': 'Контакты',
        'active_key': 'contacts',
        'meta_title': 'Контакты — аттестация рабочих мест в Беларуси',
        'meta_description': 'Оставьте заявку на аттестацию рабочих мест. Работаем по всей Беларуси. Телефон: +375 29 689-60-66.',
        'file': 'Контакты.dc.html',
    },
    # Real URL from Joomla DB (alias id=135)
    'proizvodstvennyj-kontrol-v-minske-i-belarusi-zamery-vrednykh-faktorov-v-ramkakh-laboratornogo-kontrolya': {
        'title': 'Производственный контроль',
        'active_key': 'services',
        'meta_title': 'Производственный контроль в Минске — замеры вредных факторов',
        'meta_description': 'Инструментальные замеры вредных факторов производственной среды. Собственная аккредитованная лаборатория.',
        'file': 'Производственный контроль.dc.html',
    },
    'docs': {
        'title': 'Образцы документов',
        'active_key': 'docs',
        'meta_title': 'Образцы документов для аттестации рабочих мест',
        'meta_description': 'Примеры приказов, протоколов, перечней и карт для проведения аттестации рабочих мест.',
        'file': 'Образцы документов.dc.html',
    },
    # Real URL from Joomla DB (alias id=139)
    'obrazets-prikaza-o-provedenii-attestatsii-rabochikh-mest-po-usloviyam-truda': {
        'title': 'Приказ о проведении АРМ',
        'active_key': 'docs',
        'meta_title': 'Приказ о проведении аттестации рабочих мест — образец 2022',
        'file': 'Приказ о проведении АРМ.dc.html',
    },
    # Real URL from Joomla DB (alias id=153)
    'forma-perechnya-vrednykh-i-ili-opasnykh-proizvodstvennykh-faktorov-podlezhashchikh-issledovaniyu-na-konkretnom-rabochem-meste': {
        'title': 'Перечень факторов для исследования',
        'active_key': 'docs',
        'file': 'Перечень факторов для исследования.dc.html',
    },
    # Real URL from Joomla DB (alias id=141)
    'obrazets-protokola-kolichestvennykh-izmerenij-i-raschetov-pokazatelej-tyazhesti-trudovogo-protsessa-s-primerom-zapoleneniya': {
        'title': 'Протокол по тяжести трудового процесса',
        'active_key': 'docs',
        'file': 'Протокол по тяжести.dc.html',
    },
    # Real URL from Joomla DB (alias id=143)
    'obrazets-protokola-otsenki-uslovij-truda-po-pokazatelyam-napryazhennosti-trudovogo-protsessa': {
        'title': 'Протокол по напряжённости',
        'active_key': 'docs',
        'file': 'Протокол по напряжённости.dc.html',
    },
    # Real URL from Joomla DB (alias id=152)
    'protokol-rezultatov-obsledovaniya-rabochego-mesta-v-tselyakh-proverki-na-sootvetstvie-proizvodstvennogo-oborudovaniya-i-tekhnologicheskikh-protsessov-trebovaniyam-okhrany-truda-i-zaplanirovannykh-prinyatykh-mer-po-ustraneniyu-vyyavlennykh-nedostatkov': {
        'title': 'Протокол обследования рабочего места',
        'active_key': 'docs',
        'file': 'Протокол обследования рабочего места.dc.html',
    },
    # Real URL from Joomla DB (alias id=144)
    'obrazets-protokola-zasedaniya-attestatsionnoj-komissii-o-zavershenii-raboty-po-attestatsii-rabochikh-mest-po-usloviyam-truda': {
        'title': 'Протокол о завершении АРМ',
        'active_key': 'docs',
        'file': 'Протокол о завершении АРМ.dc.html',
    },
    # Real URL from Joomla DB (alias id=145)
    'obrazets-prikaza-ob-utverzhdenii-rezultatov-attestatsii': {
        'title': 'Приказ об утверждении результатов',
        'active_key': 'docs',
        'file': 'Приказ об утверждении результатов.dc.html',
    },
    # Real URL from Joomla DB (alias id=151)
    'obrazets-plana-meropriyatij-po-uluchsheniyu-uslovij-truda-primer': {
        'title': 'План мероприятий',
        'active_key': 'docs',
        'file': 'План мероприятий.dc.html',
    },
    # Real URL from Joomla DB (alias id=140)
    'obrazets-perechnya-rabochikh-mest-podlezhashchikh-attestatsii-s-primerom-zapolneniya': {
        'title': 'Перечень рабочих мест для аттестации',
        'active_key': 'docs',
        'file': 'Перечень рабочих мест для аттестации.dc.html',
    },
    # Real URL from Joomla DB (alias id=136)
    'obrazets-perechnya-utverzhdaemogo-po-rezultatam-attestatsii-rabochikh-mest-dayushchego-pravo-na-pensiyu': {
        'title': 'Перечень на пенсию',
        'active_key': 'docs',
        'file': 'Перечень на пенсию.dc.html',
    },
    # Real URL from Joomla DB (alias id=147)
    'forma-i-obrazets-perechnya-rabochikh-mest-rabotnits-tekstilnykh-professij-dlya-tselej-professionalnogo-pensionnogo-strakhovaniya': {
        'title': 'Перечень текстильные профессии',
        'active_key': 'docs',
        'file': 'Перечень текстильные профессии.dc.html',
    },
    # Real URL from Joomla DB (alias id=148)
    'forma-i-obrazets-perechnya-rabochikh-mest-na-kotorykh-podtverzhdeno-pravo-na-dopolnitelnyj-otpusk-za-rabotu-s-vrednymi-i-ili-opasnymi-usloviyami-truda': {
        'title': 'Перечень на доп. отпуск',
        'active_key': 'docs',
        'file': 'Перечень на доп. отпуск.dc.html',
    },
    # Real URL from Joomla DB (alias id=149)
    'forma-i-obrazets-perechnya-rabochikh-mest-na-kotorykh-podtverzhdeno-pravo-na-sokrashchennuyu-prodolzhitelnost-rabochego-vremeni': {
        'title': 'Перечень на сокращение рабочего времени',
        'active_key': 'docs',
        'file': 'Перечень на сокращение рабочего времени.dc.html',
    },
    # Real URL from Joomla DB (alias id=150)
    'forma-i-obrazets-perechnya-rabochikh-mest-na-kotorykh-podtverzhdeno-pravo-na-doplaty': {
        'title': 'Перечень на доплаты',
        'active_key': 'docs',
        'file': 'Перечень на доплаты.dc.html',
    },
    # Real URL from Joomla DB (alias id=154)
    'forma-perechnya-rabochikh-mest-po-professiyam-i-dolzhnostyam-na-kotorykh-po-rezultatam-attestatsii-ne-podtverzhdeny-usloviya-truda-dayushchie-pravo-na-kompensatsii': {
        'title': 'Перечень не подтверждены условия',
        'active_key': 'docs',
        'file': 'Перечень не подтверждены условия.dc.html',
    },
    # Real URL from Joomla DB (alias id=155)
    'forma-perechnya-rabochikh-mest-meditsinskikh-rabotnikov-na-kotorykh-po-rezultatam-attestatsii-podtverzhdeny-usloviya-truda': {
        'title': 'Перечень мед. работников',
        'active_key': 'docs',
        'file': 'Перечень мед. работников.dc.html',
    },
    # Real URL from Joomla DB (menu path: obrazci-primeri-zapolneniya-kart-fotografiiy-rabochego-vremeni)
    'obrazci-primeri-zapolneniya-kart-fotografiiy-rabochego-vremeni': {
        'title': 'КФРВ по профессиям',
        'active_key': 'docs',
        'file': 'КФРВ по профессиям.dc.html',
    },
    # Real URL from Joomla DB (alias id=132)
    'kak-pravilno-zapolnyat-kartu-fotografiyu-rabochego-vremeni-obrazets-zapolneniya': {
        'title': 'Правила заполнения КФРВ',
        'active_key': 'docs',
        'file': 'Правила заполнения КФРВ.dc.html',
    },
    # Real URL from Joomla DB (alias id=131)
    'karta-fotografiya-rabochego-vremeni-s-formulami-skachat-obrazets-primer-v-excel': {
        'title': 'Карта-фотография в Excel',
        'active_key': 'docs',
        'file': 'Карта-фотография в Excel.dc.html',
    },
    # Загрузка АРМ — внешняя ссылка на ohrana-truda.by, но страница есть в дизайне
    'zagruzka-arm-v-elektronnom-vide': {
        'title': 'Загрузка АРМ в электронном виде',
        'active_key': 'docs',
        'file': 'Загрузка АРМ в электронном виде.dc.html',
    },
    # Real URL from Joomla DB (alias id=137)
    'polozheniem-o-poryadke-provedeniya-attestatsii-rabochikh-mest-po-usloviyam-truda-postanovlenie-ot-22-02-2008-253': {
        'title': 'Положение о порядке АРМ',
        'active_key': 'docs',
        'file': None,  # нет отдельного файла дизайна — создаётся через admin
    },
    # Real URL from Joomla DB (alias id=156)
    'instruktsiya-po-otsenke-uslovij-truda-pri-attestatsii-rabochikh-mest-pri-attestatsii-rabochikh-mest-po-usloviyam-truda-postanovlenie-35-ot-22-02-2008': {
        'title': 'Инструкция по оценке условий труда',
        'active_key': 'docs',
        'file': None,  # нет отдельного файла дизайна
    },
    # Real URLs from Joomla DB (aliases id=126, 128, 129)
    'attestatsiya-rabochikh-mest-stolyara-plotnika': {
        'title': 'АРМ столяра (плотника)',
        'active_key': 'docs',
        'file': 'АРМ столяра.dc.html',
    },
    'attestatsiya-rabochikh-mest-uborshchikov-territorij-dvornikov': {
        'title': 'АРМ уборщика территорий (дворника)',
        'active_key': 'docs',
        'file': 'АРМ уборщика территорий.dc.html',
    },
    'attestatsiya-rabochikh-mest-elektrogazosvarshchika': {
        'title': 'АРМ электрогазосварщика',
        'active_key': 'docs',
        'file': 'АРМ электрогазосварщика.dc.html',
    },
    'articles': {
        'title': 'Аттестация рабочих мест по профессиям',
        'active_key': '',
        'meta_title': 'Аттестация рабочих мест по профессиям — примеры',
        'meta_description': 'Примеры данных для аттестации рабочих мест: электрогазосварщик, уборщик территорий, столяр.',
        'file': 'Статьи.dc.html',
    },
}

# URL mapping: design file names → real Django URLs (matching Joomla aliases)
URL_MAP = {
    'Главная.dc.html': '/',
    'О нас.dc.html': '/about/',
    'Цены.dc.html': '/attestatsiya-rabochikh-mest-po-usloviyam-truda-v-minske-tseny-stoimost-odnogo-rabochego-mesta/',
    'Контакты.dc.html': '/contacts/',
    'Производственный контроль.dc.html': '/proizvodstvennyj-kontrol-v-minske-i-belarusi-zamery-vrednykh-faktorov-v-ramkakh-laboratornogo-kontrolya/',
    'Образцы документов.dc.html': '/docs/',
    'Приказ о проведении АРМ.dc.html': '/obrazets-prikaza-o-provedenii-attestatsii-rabochikh-mest-po-usloviyam-truda/',
    'Перечень факторов для исследования.dc.html': '/forma-perechnya-vrednykh-i-ili-opasnykh-proizvodstvennykh-faktorov-podlezhashchikh-issledovaniyu-na-konkretnom-rabochem-meste/',
    'Протокол по тяжести.dc.html': '/obrazets-protokola-kolichestvennykh-izmerenij-i-raschetov-pokazatelej-tyazhesti-trudovogo-protsessa-s-primerom-zapoleneniya/',
    'Протокол по напряжённости.dc.html': '/obrazets-protokola-otsenki-uslovij-truda-po-pokazatelyam-napryazhennosti-trudovogo-protsessa/',
    'Протокол обследования рабочего места.dc.html': '/protokol-rezultatov-obsledovaniya-rabochego-mesta-v-tselyakh-proverki-na-sootvetstvie-proizvodstvennogo-oborudovaniya-i-tekhnologicheskikh-protsessov-trebovaniyam-okhrany-truda-i-zaplanirovannykh-prinyatykh-mer-po-ustraneniyu-vyyavlennykh-nedostatkov/',
    'Протокол о завершении АРМ.dc.html': '/obrazets-protokola-zasedaniya-attestatsionnoj-komissii-o-zavershenii-raboty-po-attestatsii-rabochikh-mest-po-usloviyam-truda/',
    'Приказ об утверждении результатов.dc.html': '/obrazets-prikaza-ob-utverzhdenii-rezultatov-attestatsii/',
    'План мероприятий.dc.html': '/obrazets-plana-meropriyatij-po-uluchsheniyu-uslovij-truda-primer/',
    'Перечень рабочих мест для аттестации.dc.html': '/obrazets-perechnya-rabochikh-mest-podlezhashchikh-attestatsii-s-primerom-zapolneniya/',
    'Перечень на пенсию.dc.html': '/obrazets-perechnya-utverzhdaemogo-po-rezultatam-attestatsii-rabochikh-mest-dayushchego-pravo-na-pensiyu/',
    'Перечень текстильные профессии.dc.html': '/forma-i-obrazets-perechnya-rabochikh-mest-rabotnits-tekstilnykh-professij-dlya-tselej-professionalnogo-pensionnogo-strakhovaniya/',
    'Перечень на доп. отпуск.dc.html': '/forma-i-obrazets-perechnya-rabochikh-mest-na-kotorykh-podtverzhdeno-pravo-na-dopolnitelnyj-otpusk-za-rabotu-s-vrednymi-i-ili-opasnymi-usloviyami-truda/',
    'Перечень на сокращение рабочего времени.dc.html': '/forma-i-obrazets-perechnya-rabochikh-mest-na-kotorykh-podtverzhdeno-pravo-na-sokrashchennuyu-prodolzhitelnost-rabochego-vremeni/',
    'Перечень на доплаты.dc.html': '/forma-i-obrazets-perechnya-rabochikh-mest-na-kotorykh-podtverzhdeno-pravo-na-doplaty/',
    'Перечень не подтверждены условия.dc.html': '/forma-perechnya-rabochikh-mest-po-professiyam-i-dolzhnostyam-na-kotorykh-po-rezultatam-attestatsii-ne-podtverzhdeny-usloviya-truda-dayushchie-pravo-na-kompensatsii/',
    'Перечень мед. работников.dc.html': '/forma-perechnya-rabochikh-mest-meditsinskikh-rabotnikov-na-kotorykh-po-rezultatam-attestatsii-podtverzhdeny-usloviya-truda/',
    'КФРВ по профессиям.dc.html': '/obrazci-primeri-zapolneniya-kart-fotografiiy-rabochego-vremeni/',
    'Правила заполнения КФРВ.dc.html': '/kak-pravilno-zapolnyat-kartu-fotografiyu-rabochego-vremeni-obrazets-zapolneniya/',
    'Карта-фотография в Excel.dc.html': '/karta-fotografiya-rabochego-vremeni-s-formulami-skachat-obrazets-primer-v-excel/',
    'Загрузка АРМ в электронном виде.dc.html': '/zagruzka-arm-v-elektronnom-vide/',
    'АРМ столяра.dc.html': '/attestatsiya-rabochikh-mest-stolyara-plotnika/',
    'АРМ уборщика территорий.dc.html': '/attestatsiya-rabochikh-mest-uborshchikov-territorij-dvornikov/',
    'АРМ электрогазосварщика.dc.html': '/attestatsiya-rabochikh-mest-elektrogazosvarshchika/',
    'Статьи.dc.html': '/articles/',
}


def clean_html(raw: str) -> str:
    """Strip design-tool wrappers and fix hrefs."""
    # Remove everything outside <x-dc>...</x-dc>
    m = re.search(r'<x-dc>(.*?)</x-dc>', raw, re.DOTALL)
    if m:
        raw = m.group(1)

    # Remove <helmet>...</helmet>
    raw = re.sub(r'<helmet>.*?</helmet>', '', raw, flags=re.DOTALL)

    # Remove dc-import tags (header/footer are rendered by Django)
    raw = re.sub(r'<dc-import[^>]*/>', '', raw)
    raw = re.sub(r'<dc-import[^>]*>.*?</dc-import>', '', raw, flags=re.DOTALL)

    # Remove inline top-bar div (Главная.dc.html has it hardcoded, not via dc-import)
    # Matches the dark top bar strip
    raw = re.sub(
        r'<!-- TOP BAR -->.*?</div>\s*<!-- HEADER',
        '<!-- HEADER',
        raw, flags=re.DOTALL
    )
    # Remove inline <header>...</header> block (with nav, dropdowns, logo)
    raw = re.sub(r'<header\b[^>]*>.*?</header>', '', raw, flags=re.DOTALL)
    # Remove inline <footer>...</footer> block
    raw = re.sub(r'<footer\b[^>]*>.*?</footer>', '', raw, flags=re.DOTALL)

    # Remove sc-if tags but keep their content visible (show the first branch)
    # sc-if with hint-placeholder-val="{{ false }}" = always hidden in preview → remove entirely
    raw = re.sub(r'<sc-if[^>]*hint-placeholder-val="\{\{ false \}\}"[^>]*>.*?</sc-if>', '', raw, flags=re.DOTALL)
    # other sc-if → just unwrap
    raw = re.sub(r'<sc-if[^>]*>(.*?)</sc-if>', r'\1', raw, flags=re.DOTALL)

    # Remove template expressions {{ ... }}
    raw = re.sub(r'\{\{[^}]*\}\}', '', raw)

    # Fix hrefs: replace .dc.html links with Django URLs
    def replace_href(m):
        attr = m.group(1)  # href or src
        fname = m.group(2)
        # strip anchor
        anchor = ''
        if '#' in fname:
            fname, anchor = fname.split('#', 1)
            anchor = '#' + anchor
        url = URL_MAP.get(fname, '/' + fname.replace('.dc.html', '/').replace(' ', '-').lower())
        return f'{attr}="{url}{anchor}"'

    raw = re.sub(r'(href|src)="([^"]*\.dc\.html[^"]*)"', replace_href, raw)

    # Clean up extra blank lines
    raw = re.sub(r'\n{3,}', '\n\n', raw)

    return raw.strip()


class Command(BaseCommand):
    help = 'Import design HTML files as Django pages'

    def add_arguments(self, parser):
        parser.add_argument('design_dir', type=str, help='Path to design/project folder')

    def handle(self, *args, **options):
        import os
        design_dir = options['design_dir']

        created = 0
        updated = 0
        skipped = 0

        for slug, meta in PAGES.items():
            if not meta.get('file'):
                self.stdout.write(self.style.WARNING(f'  SKIP (no file): {slug}'))
                skipped += 1
                continue

            filepath = os.path.join(design_dir, meta['file'])
            if not os.path.exists(filepath):
                self.stdout.write(self.style.WARNING(f'  SKIP (not found): {meta["file"]}'))
                skipped += 1
                continue

            with open(filepath, encoding='utf-8') as f:
                raw = f.read()

            content = clean_html(raw)

            page, is_new = Page.objects.update_or_create(
                slug=slug,
                defaults={
                    'title': meta['title'],
                    'active_key': meta.get('active_key', ''),
                    'meta_title': meta.get('meta_title', meta['title']),
                    'meta_description': meta.get('meta_description', ''),
                    'content': content,
                    'is_published': True,
                }
            )

            if is_new:
                created += 1
                self.stdout.write(f'  CREATE: /{slug}/')
            else:
                updated += 1
                self.stdout.write(f'  UPDATE: /{slug}/')

        self.stdout.write(self.style.SUCCESS(
            f'\nDone: {created} created, {updated} updated, {skipped} skipped.'
        ))
