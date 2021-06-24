"""Local settings"""

from .base import *  # NOQA

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": str(ROOT_DIR + "db.sqlite3"),
    }
}
DATABASES["default"]["ATOMIC_REQUESTS"] = True

# Cache
CACHES = {"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache", "LOCATION": ""}}

# Email
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
EMAIL_HOST = "localhost"
EMAIL_PORT = 1025

# django-extensions
INSTALLED_APPS += ["django_extensions"]
