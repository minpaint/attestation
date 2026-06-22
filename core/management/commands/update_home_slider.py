from django.core.management.base import BaseCommand
from core.models import Page


SLIDER_HTML = """
  <!-- HERO SLIDER -->
  <section style="position:relative;overflow:hidden;background:linear-gradient(180deg,#f3f6ff,#fff);">
    <div id="heroTrack" style="display:flex;width:100%;transition:transform .6s cubic-bezier(.7,0,.2,1);">

      <!-- slide 1 -->
      <div style="flex:0 0 100%;display:grid;grid-template-columns:1.05fr .95fr;gap:30px;align-items:center;padding:56px 48px;">
        <div>
          <div style="display:inline-flex;align-items:center;gap:8px;background:#fff0e6;color:#d2540a;padding:7px 14px;border-radius:30px;font:700 12px/1 'Manrope';letter-spacing:.4px;margin-bottom:18px;">● ПОД КЛЮЧ · МИНСК И ВСЯ БЕЛАРУСЬ</div>
          <h1 style="font:800 46px/1.08 'Manrope';margin:0 0 16px;color:#0c1733;letter-spacing:-.6px;">Аттестация рабочих мест</h1>
          <p style="font:400 17px/1.6 'Manrope';color:#4a526b;margin:0 0 26px;max-width:500px;">Мы осуществляем проведение полного комплекса работ по аттестации рабочих мест по условиям труда «под ключ» с оформлением исчерпывающего комплекта документации именно для Вашей организации.</p>
          <a href="/contacts/" class="btnA" style="display:inline-block;background:#ff6a13;color:#fff;padding:15px 28px;border-radius:9px;font:700 15px/1 'Manrope';text-decoration:none;">Подать заявку!</a>
        </div>
        <div style="display:flex;justify-content:center;"><img src="/static/img/generated/hero-attestation.png" alt="Workplace attestation specialists" style="width:100%;max-width:520px;height:320px;object-fit:cover;border-radius:18px;box-shadow:0 24px 60px rgba(12,23,51,.16);"></div>
      </div>

      <!-- slide 2 -->
      <div style="flex:0 0 100%;display:grid;grid-template-columns:1.05fr .95fr;gap:30px;align-items:center;padding:56px 48px;">
        <div>
          <div style="display:inline-flex;align-items:center;gap:8px;background:#fff0e6;color:#d2540a;padding:7px 14px;border-radius:30px;font:700 12px/1 'Manrope';letter-spacing:.4px;margin-bottom:18px;">● БОЛЬШАЯ ОБЛАСТЬ АККРЕДИТАЦИИ</div>
          <h1 style="font:800 46px/1.08 'Manrope';margin:0 0 16px;color:#0c1733;letter-spacing:-.6px;">Собственная лаборатория</h1>
          <p style="font:400 17px/1.6 'Manrope';color:#4a526b;margin:0 0 26px;max-width:500px;">Наша лаборатория имеет большую степень аккредитации — мы готовы выполнить все виды замеров, произведём оценку уровней вредных факторов, оформим протоколы замеров установленной формы.</p>
          <a href="/contacts/" class="btnA" style="display:inline-block;background:#ff6a13;color:#fff;padding:15px 28px;border-radius:9px;font:700 15px/1 'Manrope';text-decoration:none;">Заказать замеры!</a>
        </div>
        <div style="display:flex;justify-content:center;"><img src="/static/img/generated/hero-laboratory.png" alt="Accredited laboratory measurements" style="width:100%;max-width:520px;height:320px;object-fit:cover;border-radius:18px;box-shadow:0 24px 60px rgba(12,23,51,.16);"></div>
      </div>

      <!-- slide 3 -->
      <div style="flex:0 0 100%;display:grid;grid-template-columns:1.05fr .95fr;gap:30px;align-items:center;padding:56px 48px;">
        <div>
          <div style="display:inline-flex;align-items:center;gap:8px;background:#fff0e6;color:#d2540a;padding:7px 14px;border-radius:30px;font:700 12px/1 'Manrope';letter-spacing:.4px;margin-bottom:18px;">● ГОТОВО ДЛЯ ГОСЭКСПЕРТИЗЫ</div>
          <h1 style="font:800 46px/1.08 'Manrope';margin:0 0 16px;color:#0c1733;letter-spacing:-.6px;">Модуль электронной формы</h1>
          <p style="font:400 17px/1.6 'Manrope';color:#4a526b;margin:0 0 26px;max-width:500px;">Мы загрузим результаты аттестации в специализированное ПО «Модуль электронной формы» — Вам останется лишь подписать и отправить файл в государственную экспертизу.</p>
          <a href="/contacts/" class="btnA" style="display:inline-block;background:#ff6a13;color:#fff;padding:15px 28px;border-radius:9px;font:700 15px/1 'Manrope';text-decoration:none;">Заказать аттестацию!</a>
        </div>
        <div style="display:flex;justify-content:center;"><img src="/static/img/generated/hero-electronic-module.png" alt="Electronic workplace attestation documents" style="width:100%;max-width:520px;height:320px;object-fit:cover;border-radius:18px;box-shadow:0 24px 60px rgba(12,23,51,.16);"></div>
      </div>
    </div>

    <!-- dots -->
    <div style="position:absolute;bottom:22px;left:48px;display:flex;gap:9px;">
      <span id="dot0" onclick="goTo(0)" style="width:34px;height:5px;border-radius:3px;cursor:pointer;background:#ff6a13;"></span>
      <span id="dot1" onclick="goTo(1)" style="width:34px;height:5px;border-radius:3px;cursor:pointer;background:#c8d3ed;"></span>
      <span id="dot2" onclick="goTo(2)" style="width:34px;height:5px;border-radius:3px;cursor:pointer;background:#c8d3ed;"></span>
    </div>
  </section>

  <script>
    (function(){
      var current = 0;
      var total = 3;
      var timer;

      function goTo(n) {
        current = n;
        document.getElementById('heroTrack').style.transform = 'translateX(-' + (n * 100) + '%)';
        ['dot0','dot1','dot2'].forEach(function(id, i) {
          document.getElementById(id).style.background = i === n ? '#ff6a13' : '#c8d3ed';
        });
        resetTimer();
      }

      function next() { goTo((current + 1) % total); }

      function resetTimer() {
        clearInterval(timer);
        timer = setInterval(next, 5000);
      }

      window.goTo = goTo;
      resetTimer();
    })();
  </script>
"""


class Command(BaseCommand):
    help = 'Fix hero slider on home page'

    def handle(self, *args, **options):
        page = Page.objects.get(slug='home')
        content = page.content

        # Replace the broken slider section with working JS slider
        import re
        # Find from <!-- HERO SLIDER --> to end of </script> after the slider
        new_content = re.sub(
            r'<!-- HERO SLIDER -->.*?</script>',
            SLIDER_HTML.strip(),
            content,
            flags=re.DOTALL,
            count=1,
        )

        if new_content == content:
            self.stdout.write(self.style.WARNING('Pattern not found — replacing full slider section by marker'))
            # fallback: replace from the section tag containing heroTrack
            new_content = re.sub(
                r'<section[^>]*>.*?id="heroTrack".*?</section>\s*(<script>.*?</script>)?',
                SLIDER_HTML.strip(),
                content,
                flags=re.DOTALL,
                count=1,
            )

        page.content = new_content
        page.save()
        self.stdout.write(self.style.SUCCESS('Home slider fixed.'))
