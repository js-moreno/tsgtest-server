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


# Email
EMAIL_BACKEND = env("EMAIL_BACKEND")
EMAIL_HOST = env("EMAIL_HOST")
EMAIL_PORT = env("EMAIL_PORT")
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL")

# CORS
INSTALLED_APPS += ["corsheaders"]

MIDDLEWARE.insert(1, "corsheaders.middleware.CorsMiddleware")

CORS_ORIGIN_ALLOW_ALL = env.bool("CORS_ORIGIN_ALLOW_ALL", True)

if not CORS_ORIGIN_ALLOW_ALL:
    CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS")


CORS_ALLOW_HEADERS = list(default_headers)

CORS_EXPOSE_HEADERS = ["Content-Disposition"]
