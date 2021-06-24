"""Users urls"""

# Django rest framework
from rest_framework.routers import SimpleRouter

# Accounts
from apps.accounts import views

router = SimpleRouter()
router.register(r"users", views.UserViewSet, basename="users")