"""Security response headers, including a Content-Security-Policy.

The site renders a lot of inline <style> and inline <script> (both in the base
template and inside stored page HTML), so the policy intentionally allows
'unsafe-inline' for styles and scripts — a stricter nonce-based policy would
require rewriting every inline block. Even so, the policy still meaningfully
hardens the site:

  * default-src 'self'      → no resources from arbitrary third parties
  * script-src whitelist    → blocks injected <script src="evil.com">
  * object-src 'none'       → no Flash/embeds
  * base-uri 'self'         → blocks <base> tag hijacking
  * frame-ancestors 'none'  → clickjacking protection (modern equivalent of
                              X-Frame-Options)
  * form-action 'self'      → forms can only submit back to this origin
"""

from django.conf import settings


def build_csp():
    fonts = "https://fonts.gstatic.com"
    styles_css = "https://fonts.googleapis.com"
    directives = [
        "default-src 'self'",
        # inline scripts are used throughout the templates/content
        "script-src 'self' 'unsafe-inline'",
        f"style-src 'self' 'unsafe-inline' {styles_css}",
        f"font-src 'self' {fonts} data:",
        "img-src 'self' data: https:",
        f"connect-src 'self'",
        "object-src 'none'",
        "base-uri 'self'",
        "frame-ancestors 'none'",
        "form-action 'self'",
    ]
    if not settings.DEBUG:
        directives.append("upgrade-insecure-requests")
    return "; ".join(directives)


class SecurityHeadersMiddleware:
    """Adds CSP and a few defensive headers to every response."""

    def __init__(self, get_response):
        self.get_response = get_response
        self.csp = build_csp()

    def __call__(self, request):
        response = self.get_response(request)
        response.setdefault('Content-Security-Policy', self.csp)
        # Defensive extras (some overlap with Django's SecurityMiddleware in prod,
        # but harmless and useful in any mode).
        response.setdefault('X-Content-Type-Options', 'nosniff')
        response.setdefault('Referrer-Policy', 'same-origin')
        response.setdefault('X-Frame-Options', 'DENY')
        response.setdefault(
            'Permissions-Policy',
            'geolocation=(), microphone=(), camera=(), payment=()',
        )
        return response
