# apps.core.views.py
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils.html import escape

def _add_security_headers(response):
    """
    Add extra security-related headers to responses.
    Some headers (HSTS, Secure cookies, X-Frame-Options) are configured from settings
    as well, but adding them here provides defense-in-depth.
    """
    # Prevent MIME sniffing
    response.setdefault("X-Content-Type-Options", "nosniff")
    # Clickjacking protection (also controlled by X_FRAME_OPTIONS in settings)
    response.setdefault("X-Frame-Options", getattr(settings, "X_FRAME_OPTIONS", "DENY"))
    # Referrer policy
    response.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
    # Basic XSS protection header (mostly legacy but harmless)
    response.setdefault("X-XSS-Protection", "1; mode=block")
    # Permissions policy: restrict access to powerful features
    response.setdefault("Permissions-Policy", "geolocation=(), microphone=(), camera=()")
    # A minimal Content Security Policy — keep it conservative and update for your assets.
    # Note: if your app loads resources from other domains (CDNs, frontend host), update CSP accordingly.
    csp = "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:;"
    response.setdefault("Content-Security-Policy", csp)

    # Add HSTS only if Django settings indicate HSTS is enabled (avoid adding during dev)
    try:
        if not settings.DEBUG and getattr(settings, "SECURE_HSTS_SECONDS", 0) > 0:
            response.setdefault("Strict-Transport-Security", f"max-age={settings.SECURE_HSTS_SECONDS}; includeSubDomains; preload")
    except Exception:
        # fail-safe: don't raise if settings are not present
        pass

    return response


def home(request):
    """
    Homepage view — uses a template (safer than embedding HTML in Python).
    The view exposes minimal info and never prints secret/internal values.
    """
    # Use reverse to find the admin index URL rather than hardcoding it.
    try:
        admin_url = reverse('admin:index')
    except Exception:
        admin_url = "/admin/"  # fallback

    # Keep the context minimal and escaped where needed
    context = {
        "site_name": "Spa Central",
        "admin_url": admin_url,
        # never pass secrets or environment data here
    }
    response = render(request, "home.html", context=context, status=200)
    return _add_security_headers(response)


def health_check(request):
    """
    Simple health check endpoint for load balancers/uptime monitors.
    Returns minimal JSON and 200 when app is healthy.
    Do NOT expose detailed internals or DB credentials here.
    """
    # Optionally you can check DB, cache, redis etc. and return 200/503 accordingly.
    payload = {"status": "ok"}
    response = JsonResponse(payload, status=200)
    return _add_security_headers(response)


def custom_404(request, exception=None):
    """Custom 404 handler — render a friendly page and avoid debug details."""
    response = render(request, "404.html", status=404)
    return _add_security_headers(response)


def custom_500(request):
    """Custom 500 handler — do NOT reveal exception details in the response."""
    response = render(request, "500.html", status=500)
    return _add_security_headers(response)
