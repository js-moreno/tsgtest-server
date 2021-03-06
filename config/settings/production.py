"""Production settings."""

from .base import *  # NOQA
from corsheaders.defaults import default_headers

# Database
DATABASES = {
    "default": {
        "ENGINE": env("DB_ENGINE"),
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST"),
        "PORT": env("DB_PORT"),
    }
}
DATABASES["default"]["ATOMIC_REQUESTS"] = True
DATABASES["default"]["CONN_MAX_AGE"] = env.int("CONN_MAX_AGE", default=60)

# WhiteNoise
MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")

# Static  files
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# CORS
INSTALLED_APPS += ["corsheaders"]

MIDDLEWARE.insert(1, "corsheaders.middleware.CorsMiddleware")

CORS_ORIGIN_ALLOW_ALL = env.bool("CORS_ORIGIN_ALLOW_ALL", True)

if not CORS_ORIGIN_ALLOW_ALL:
    CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS")


CORS_ALLOW_HEADERS = list(default_headers)

CORS_EXPOSE_HEADERS = ["Content-Disposition"]
