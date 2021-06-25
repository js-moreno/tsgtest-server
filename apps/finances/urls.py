"""Credit card urls"""

# Django rest framework
from rest_framework.routers import SimpleRouter

# Accounts
from apps.finances import views

router = SimpleRouter()
router.register(r"credit-cards", views.CreditCardViewSet, basename="credit_card")