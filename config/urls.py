"""tsgtest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# Django
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.views.generic.base import RedirectView

# Django rest framework
from rest_framework.routers import DefaultRouter

# Urls
from documentation.urls import url_documentation

# Routers
from apps.accounts.urls import router as router_accounts

router = DefaultRouter(trailing_slash=False)
router.registry.extend(router_accounts.registry)

# Administration site
admin.site.site_header = settings.APP_NAME
admin.site.site_title = settings.APP_NAME
admin.site.site_url = "/documentation"

urlpatterns = [
    path("", RedirectView.as_view(url="documentation/", permanent=False), name="index"),
    path("", include((url_documentation, "documentation"), namespace="documentation")),
    path("admin/", admin.site.urls),
    path("", include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
