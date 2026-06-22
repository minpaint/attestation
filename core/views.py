import os
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.core.cache import cache
from django.conf import settings
from .models import Page


def _client_ip(request):
    """Best-effort client IP, honouring a single reverse proxy."""
    xff = request.META.get('HTTP_X_FORWARDED_FOR', '')
    if xff:
        return xff.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', '') or 'unknown'


def _extract_summary(content):
    """Вытаскивает первый непустой абзац из HTML-контента."""
    import re
    for m in re.finditer(r'<p[^>]*>(.*?)</p>', content, re.DOTALL):
        text = re.sub(r'<[^>]+>', '', m.group(1)).strip()
        if len(text) > 40:
            return text[:220] + ('…' if len(text) > 220 else '')
    return ''


def _page_ctx(request, page):
    ctx = {'page': page}
    if request.user.is_staff:
        from django.urls import reverse
        ctx['admin_edit_url'] = reverse('admin:core_page_change', args=[page.pk])
    # Если страница является агрегатором — загружаем дочерние страницы
    children = Page.objects.filter(category=page.slug, is_published=True).order_by('title')
    if children.exists():
        child_list = []
        for ch in children:
            child_list.append({
                'page': ch,
                'summary': ch.summary or _extract_summary(ch.content),
            })
        ctx['child_pages'] = child_list
    return ctx


def page_view(request, slug=''):
    if not slug:
        slug = 'home'
    page = get_object_or_404(Page, slug=slug, is_published=True)
    return render(request, 'core/page.html', _page_ctx(request, page))


def page_view_html(request, slug=''):
    """Serve old Joomla .html URLs without redirect — same page, same status."""
    page = get_object_or_404(Page, slug=slug, is_published=True)
    return render(request, 'core/page.html', _page_ctx(request, page))


@csrf_exempt
@require_POST
def contact_form(request):
    import json
    try:
        data = json.loads(request.body)
    except Exception:
        data = request.POST.dict()

    # Honeypot: a hidden field real users never fill. Bots tend to fill every
    # field — if it has content, silently accept (return ok) and drop the message.
    if (data.get('website', '') or data.get('fax', '')).strip():
        return JsonResponse({'ok': True})

    org      = data.get('org', '').strip()
    contact  = data.get('contact', '').strip()
    phone    = data.get('phone', '').strip()
    email    = data.get('email', '').strip()
    city     = data.get('city', '').strip()
    count    = data.get('count', '').strip()
    comment  = data.get('comment', '').strip()

    if not phone and not email:
        return JsonResponse({'ok': False, 'error': 'Укажите телефон или email'}, status=400)

    # Per-IP rate limiting (cache-backed) to curb spam/flooding.
    limit = getattr(settings, 'CONTACT_RATE_LIMIT', 5)
    window = getattr(settings, 'CONTACT_RATE_WINDOW', 3600)
    cache_key = f'contact_rl:{_client_ip(request)}'
    count_so_far = cache.get(cache_key, 0)
    if count_so_far >= limit:
        return JsonResponse(
            {'ok': False, 'error': 'Слишком много заявок. Попробуйте позже или позвоните нам.'},
            status=429,
        )
    # Increment with a fresh TTL on first hit in the window.
    if count_so_far == 0:
        cache.set(cache_key, 1, window)
    else:
        try:
            cache.incr(cache_key)
        except ValueError:
            cache.set(cache_key, 1, window)

    # Basic length guard against abuse / oversized payloads.
    for field in (org, contact, phone, email, city, count, comment):
        if len(field) > 2000:
            return JsonResponse({'ok': False, 'error': 'Слишком длинное значение в форме.'}, status=400)

    body = f"""Новая заявка с сайта attestation.by
{'─' * 40}
Организация:        {org or '—'}
Контактное лицо:    {contact or '—'}
Телефон:            {phone or '—'}
E-mail:             {email or '—'}
Город / район:      {city or '—'}
Рабочих мест:       {count or '—'}
Комментарий:        {comment or '—'}
{'─' * 40}
"""

    recipient = getattr(settings, 'CONTACT_EMAIL', '') or getattr(settings, 'EMAIL_HOST_USER', '')

    errors = []

    # Send email
    try:
        send_mail(
            subject=f'Заявка на аттестацию — {org or contact or phone}',
            message=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient],
            fail_silently=False,
        )
    except Exception as e:
        errors.append(str(e))

    # Send Telegram notification (optional — only if credentials are set)
    tg_token = os.environ.get('TELEGRAM_BOT_TOKEN', '')
    tg_chat  = os.environ.get('TELEGRAM_CHAT_ID', '')
    if tg_token and tg_chat:
        try:
            import urllib.request, urllib.parse
            tg_text = (
                f"\U0001f4cb *Новая заявка* — attestation.by\n"
                f"{'─' * 30}\n"
                f"*Организация:* {org or '—'}\n"
                f"*Контакт:* {contact or '—'}\n"
                f"*Телефон:* {phone or '—'}\n"
                f"*E-mail:* {email or '—'}\n"
                f"*Город:* {city or '—'}\n"
                f"*Рабочих мест:* {count or '—'}\n"
                f"*Комментарий:* {comment or '—'}"
            )
            payload = urllib.parse.urlencode({
                'chat_id': tg_chat,
                'text': tg_text,
                'parse_mode': 'Markdown',
            }).encode()
            req = urllib.request.Request(
                f'https://api.telegram.org/bot{tg_token}/sendMessage',
                data=payload, method='POST'
            )
            urllib.request.urlopen(req, timeout=5)
        except Exception as e:
            errors.append(f'Telegram: {e}')

    if not errors:
        return JsonResponse({'ok': True})
    # If email failed but Telegram succeeded (or vice versa) — still report success
    # to user; log errors server-side. Only fail if BOTH channels failed.
    if len(errors) >= 2 or (not tg_token and errors):
        return JsonResponse({'ok': False, 'error': errors[0]}, status=500)
    return JsonResponse({'ok': True})
