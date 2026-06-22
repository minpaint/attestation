from django.core.management.base import BaseCommand
from core.models import Page

CONTENT = """
<div style="font-family:'Manrope',sans-serif;color:#16285a;background:#fff;max-width:1280px;margin:0 auto;box-shadow:0 0 60px rgba(12,23,51,.08);">

  <!-- HERO -->
  <section style="background:linear-gradient(120deg,#0c1733,#1c2f60);color:#fff;padding:56px 48px 52px;">
    <div style="font:600 13px/1 'Manrope';color:#9fb0d8;margin-bottom:16px;"><a href="/" style="color:#9fb0d8;text-decoration:none;">Главная</a> &nbsp;/&nbsp; Контакты</div>
    <h1 style="font:800 40px/1.1 'Manrope';margin:0 0 16px;letter-spacing:-.5px;">Работаем по всей Беларуси</h1>
    <p style="font:400 17px/1.6 'Manrope';color:#c3cfe8;margin:0;max-width:680px;">Наши специалисты выезжают к вам — в любой город, район или предприятие на территории Республики Беларусь.</p>
  </section>

  <!-- MAIN: FORM LEFT + CONTACTS RIGHT -->
  <section style="padding:48px 48px 60px;display:grid;grid-template-columns:1.1fr 0.9fr;gap:36px;align-items:start;">

    <!-- LEFT: FORM -->
    <div style="background:#f5f8ff;border:1px solid #e6ebf5;border-radius:18px;padding:36px;">
      <h2 style="font:800 22px/1.3 'Manrope';color:#0c1733;margin:0 0 6px;">Оставить заявку</h2>
      <p style="font:400 14.5px/1.6 'Manrope';color:#5a627b;margin:0 0 24px;">Заполните форму — менеджер свяжется с вами в течение рабочего дня.</p>
      <div style="display:flex;flex-direction:column;gap:13px;">
        <input placeholder="Организация / ИП" style="padding:14px 15px;border:1px solid #d3dbec;border-radius:9px;font:400 14.5px/1 'Manrope';color:#16285a;background:#fff;outline:none;width:100%;" />
        <input placeholder="Контактное лицо" style="padding:14px 15px;border:1px solid #d3dbec;border-radius:9px;font:400 14.5px/1 'Manrope';color:#16285a;background:#fff;outline:none;width:100%;" />
        <input placeholder="Телефон" style="padding:14px 15px;border:1px solid #d3dbec;border-radius:9px;font:400 14.5px/1 'Manrope';color:#16285a;background:#fff;outline:none;width:100%;" />
        <input placeholder="E-mail" style="padding:14px 15px;border:1px solid #d3dbec;border-radius:9px;font:400 14.5px/1 'Manrope';color:#16285a;background:#fff;outline:none;width:100%;" />
        <input placeholder="Город / район" style="padding:14px 15px;border:1px solid #d3dbec;border-radius:9px;font:400 14.5px/1 'Manrope';color:#16285a;background:#fff;outline:none;width:100%;" />
        <div style="border:1.5px dashed #c2cce4;border-radius:9px;padding:14px 15px;font:400 14px/1.4 'Manrope';color:#8893b3;background:#fff;cursor:pointer;">📎 Прикрепить штатное расписание</div>
        <textarea placeholder="Комментарий (кол-во рабочих мест, особые условия)" rows="3" style="padding:14px 15px;border:1px solid #d3dbec;border-radius:9px;font:400 14.5px/1.4 'Manrope';color:#16285a;background:#fff;resize:none;outline:none;width:100%;"></textarea>
        <div style="background:#ff6a13;color:#fff;text-align:center;padding:16px;border-radius:9px;font:800 15px/1 'Manrope';cursor:pointer;transition:transform .15s ease,box-shadow .15s ease;" onmouseover="this.style.transform='translateY(-2px)';this.style.boxShadow='0 12px 28px rgba(255,106,19,.34)'" onmouseout="this.style.transform='';this.style.boxShadow=''">Подать заявку на аттестацию!</div>
        <div style="text-align:center;font:400 12.5px/1.5 'Manrope';color:#9aa3bd;">Ответим в течение 1 рабочего дня · Работаем по всей Беларуси</div>
      </div>
    </div>

    <!-- RIGHT: CONTACTS CARD -->
    <div style="border:1px solid #e6ebf5;border-radius:18px;overflow:hidden;">

      <!-- ТЕЛЕФОНЫ — первыми -->
      <div style="padding:28px 28px 22px;border-bottom:1px solid #e6ebf5;">
        <div style="font:700 11px/1 'IBM Plex Mono',monospace;color:#ff6a13;letter-spacing:1px;text-transform:uppercase;margin-bottom:14px;">Телефоны</div>
        <a href="tel:+375296896066" style="display:block;font:800 22px/1.3 'Manrope';color:#16285a;text-decoration:none;margin-bottom:4px;">+375 29 689-60-66</a>
        <div style="font:500 12px/1 'IBM Plex Mono',monospace;color:#8a91a6;margin-bottom:14px;">Velcom / A1</div>
        <a href="tel:+375336816066" style="display:block;font:800 22px/1.3 'Manrope';color:#16285a;text-decoration:none;margin-bottom:4px;">+375 33 681-60-66</a>
        <div style="font:500 12px/1 'IBM Plex Mono',monospace;color:#8a91a6;">MTS</div>
      </div>

      <!-- EMAIL -->
      <div style="padding:22px 28px;border-bottom:1px solid #e6ebf5;">
        <div style="font:700 11px/1 'IBM Plex Mono',monospace;color:#8a91a6;letter-spacing:1px;text-transform:uppercase;margin-bottom:10px;">Электронная почта</div>
        <a href="mailto:6896066@tut.by" style="font:700 16px/1 'Manrope';color:#16285a;text-decoration:none;">6896066@tut.by</a>
        <div style="margin-top:8px;font:400 13px/1.5 'Manrope';color:#8a91a6;">Пришлите штатное расписание — рассчитаем стоимость</div>
      </div>

      <!-- РЕЖИМ РАБОТЫ -->
      <div style="padding:22px 28px;border-bottom:1px solid #e6ebf5;">
        <div style="font:700 11px/1 'IBM Plex Mono',monospace;color:#8a91a6;letter-spacing:1px;text-transform:uppercase;margin-bottom:10px;">Режим работы</div>
        <div style="font:700 15px/1.5 'Manrope';color:#16285a;">Пн–Сб: 9:00–21:00</div>
        <div style="font:500 13px/1.5 'Manrope';color:#5a627b;">Воскресенье — выходной</div>
      </div>

      <!-- ОРГАНИЗАЦИЯ -->
      <div style="padding:22px 28px;border-bottom:1px solid #e6ebf5;">
        <div style="font:700 11px/1 'IBM Plex Mono',monospace;color:#8a91a6;letter-spacing:1px;text-transform:uppercase;margin-bottom:10px;">Организация</div>
        <div style="font:700 15px/1.4 'Manrope';color:#16285a;">ООО «Политех-оптимал»</div>
        <div style="font:400 13px/1.5 'Manrope';color:#8a91a6;margin-top:4px;">Выезд к заказчику по всей стране</div>
      </div>

      <!-- РЕГИОНЫ -->
      <div style="padding:22px 28px;">
        <div style="font:700 11px/1 'IBM Plex Mono',monospace;color:#8a91a6;letter-spacing:1px;text-transform:uppercase;margin-bottom:12px;">Регионы присутствия</div>
        <div style="display:flex;flex-wrap:wrap;gap:7px;">
          <span style="background:#f5f8ff;border:1px solid #e6ebf5;border-radius:7px;padding:7px 11px;font:600 12.5px/1 'Manrope';color:#16285a;">Минск</span>
          <span style="background:#f5f8ff;border:1px solid #e6ebf5;border-radius:7px;padding:7px 11px;font:600 12.5px/1 'Manrope';color:#16285a;">Минская обл.</span>
          <span style="background:#f5f8ff;border:1px solid #e6ebf5;border-radius:7px;padding:7px 11px;font:600 12.5px/1 'Manrope';color:#16285a;">Брест</span>
          <span style="background:#f5f8ff;border:1px solid #e6ebf5;border-radius:7px;padding:7px 11px;font:600 12.5px/1 'Manrope';color:#16285a;">Брестская обл.</span>
          <span style="background:#f5f8ff;border:1px solid #e6ebf5;border-radius:7px;padding:7px 11px;font:600 12.5px/1 'Manrope';color:#16285a;">Гродно</span>
          <span style="background:#f5f8ff;border:1px solid #e6ebf5;border-radius:7px;padding:7px 11px;font:600 12.5px/1 'Manrope';color:#16285a;">Гродненская обл.</span>
          <span style="background:#f5f8ff;border:1px solid #e6ebf5;border-radius:7px;padding:7px 11px;font:600 12.5px/1 'Manrope';color:#16285a;">Витебск</span>
          <span style="background:#f5f8ff;border:1px solid #e6ebf5;border-radius:7px;padding:7px 11px;font:600 12.5px/1 'Manrope';color:#16285a;">Витебская обл.</span>
          <span style="background:#f5f8ff;border:1px solid #e6ebf5;border-radius:7px;padding:7px 11px;font:600 12.5px/1 'Manrope';color:#16285a;">Могилёв</span>
          <span style="background:#f5f8ff;border:1px solid #e6ebf5;border-radius:7px;padding:7px 11px;font:600 12.5px/1 'Manrope';color:#16285a;">Могилёвская обл.</span>
          <span style="background:#f5f8ff;border:1px solid #e6ebf5;border-radius:7px;padding:7px 11px;font:600 12.5px/1 'Manrope';color:#16285a;">Гомель</span>
          <span style="background:#f5f8ff;border:1px solid #e6ebf5;border-radius:7px;padding:7px 11px;font:600 12.5px/1 'Manrope';color:#16285a;">Гомельская обл.</span>
        </div>
      </div>

    </div>
  </section>

  <!-- КАК МЫ РАБОТАЕМ -->
  <section style="padding:0 48px 60px;">
    <div style="border:1px solid #e6ebf5;border-radius:18px;padding:36px 40px;">
      <div style="font:800 12px/1 'IBM Plex Mono',monospace;letter-spacing:1.5px;color:#ff6a13;text-transform:uppercase;margin-bottom:20px;">Как мы работаем</div>
      <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:28px;">
        <div style="display:flex;gap:18px;align-items:flex-start;">
          <div style="flex:none;width:40px;height:40px;border-radius:50%;background:#16285a;color:#fff;display:flex;align-items:center;justify-content:center;font:800 16px/1 'Manrope';">1</div>
          <div>
            <div style="font:700 15px/1.3 'Manrope';color:#16285a;margin-bottom:5px;">Вы присылаете штатное расписание</div>
            <div style="font:400 13.5px/1.55 'Manrope';color:#5a627b;">На e-mail или передаёте при звонке — это отправная точка для расчёта</div>
          </div>
        </div>
        <div style="display:flex;gap:18px;align-items:flex-start;">
          <div style="flex:none;width:40px;height:40px;border-radius:50%;background:#16285a;color:#fff;display:flex;align-items:center;justify-content:center;font:800 16px/1 'Manrope';">2</div>
          <div>
            <div style="font:700 15px/1.3 'Manrope';color:#16285a;margin-bottom:5px;">Мы рассчитываем стоимость и сроки</div>
            <div style="font:400 13.5px/1.55 'Manrope';color:#5a627b;">Коммерческое предложение готовим в течение 1 рабочего дня</div>
          </div>
        </div>
        <div style="display:flex;gap:18px;align-items:flex-start;">
          <div style="flex:none;width:40px;height:40px;border-radius:50%;background:#ff6a13;color:#fff;display:flex;align-items:center;justify-content:center;font:800 16px/1 'Manrope';">3</div>
          <div>
            <div style="font:700 15px/1.3 'Manrope';color:#16285a;margin-bottom:5px;">Наши специалисты выезжают к вам</div>
            <div style="font:400 13.5px/1.55 'Manrope';color:#5a627b;">Проводим все работы «под ключ» — вам остаётся только подписать</div>
          </div>
        </div>
      </div>
    </div>
  </section>

</div>
"""


class Command(BaseCommand):
    help = 'Update contacts page layout'

    def handle(self, *args, **options):
        page, created = Page.objects.update_or_create(
            slug='contacts',
            defaults={
                'title': 'Контакты',
                'nav_key': 'contacts',
                'meta_title': 'Контакты — Аттестация рабочих мест в Беларуси',
                'meta_description': 'Оставьте заявку на аттестацию рабочих мест. Работаем по всей Беларуси. Телефон: +375 29 689-60-66.',
                'content': CONTENT.strip(),
                'is_published': True,
            }
        )
        self.stdout.write(self.style.SUCCESS('Contacts page updated.'))
