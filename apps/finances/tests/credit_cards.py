"""Credit card tests"""

# Django
from django.db.models import Q
from django.urls import reverse
from django.db import connection
from rest_framework import status
from django.utils.translation import gettext as _

# Django Rest Framework
from rest_framework.test import APITestCase

# Accounts apps
from apps.accounts.models import User
from apps.accounts.tests.users import UserFactory

# Finances apps
from apps.finances.models import CreditCard
from apps.finances.utils import CreditCardFranchises

# Factory boy
import factory

# Utils
import json
import random


class CreditCardFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CreditCard

    number = factory.Faker("credit_card_number")
    franchise = random.choice(CreditCardFranchises.choices)[0]
    due_date_year = factory.Faker("random_int", min=2020, max=2030)
    due_date_month = factory.Faker("random_int", min=1, max=12)
    verification_code = factory.Faker("credit_card_security_code")
    is_principal = factory.Faker("boolean")
    user = factory.Iterator(User.objects.all())


class CreditCardsTests(APITestCase):
    """Credit card test case"""

    def setUp(self):
        """Test case setup"""
        UserFactory.create_batch(5)
        CreditCardFactory.create_batch(5)

    def test_sensitiveDataSavedEncrypted(self):
        credit_card = CreditCard.objects.order_by("?").first()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM finances_creditcard WHERE id = %s", [credit_card.id])
            columns = [col[0] for col in cursor.description]
            row = cursor.fetchone()
            sql_data = dict(zip(columns, row))
        self.assertNotEqual(credit_card.number, sql_data["number"])
        self.assertNotEqual(credit_card.verification_code, sql_data["verification_code"])

    def test_onlyOnePrincipal(self):
        user = User.objects.order_by("?").first()
        credit_card1 = CreditCardFactory(user=user, is_principal=True)
        credit_card2 = CreditCardFactory(user=user, is_principal=True)
        credit_card3 = CreditCardFactory(user=user, is_principal=True)
        self.assertEqual(CreditCard.objects.filter(user=user, is_principal=True).count(), 1)
        self.assertEqual(CreditCard.objects.get(user=user, is_principal=True).id, credit_card3.id)
        credit_card1.refresh_from_db()
        credit_card2.refresh_from_db()
        self.assertFalse(credit_card1.is_principal)
        self.assertFalse(credit_card2.is_principal)

    def test_listCreditCards(self):
        """
        Check credit card list
        """
        url = reverse("credit_card-list")

        # Super user
        user = User.objects.create_user(email="superuser@example.com", is_superuser=True)
        self.client.force_authenticate(user=user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotContains(response, "verification_code")  # Sensitive data
        data = json.loads(response.content)["data"]
        for i in data:
            self.assertFalse("number" in i["attributes"])  # Sensitive data exact attribute
        self.assertEqual(
            len(json.loads(response.content)["data"]),
            CreditCard.objects.all().count(),
        )

        # Standard user
        user = User.objects.create_user(email="standarduser@example.com")
        self.client.force_authenticate(user=user)
        response_trucated = self.client.get(url)
        self.assertEqual(response_trucated.status_code, status.HTTP_200_OK)
        data = json.loads(response_trucated.content)["data"]
        self.assertEqual(
            len(json.loads(response_trucated.content)["data"]),
            CreditCard.objects.filter(user=user).count(),
        )
        self.assertNotContains(response_trucated, "verification_code")  # Sensitive data
        for i in data:
            self.assertEqual(i["relationships"]["user"]["data"]["id"], str(user.id))  # Own data
            self.assertFalse("number" in i["attributes"])  # Sensitive data exact attribute

        # Anonymous user
        self.client.force_authenticate(user=None)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_updateCreditCardsForbidden(self):
        """
        Check edition forbidden
        """
        user = User.objects.create_user(email="superuser@example.com", is_superuser=True)
        self.client.force_authenticate(user=user)
        credit_card = CreditCard.objects.order_by("?").first()
        url = reverse("credit_card-detail", kwargs={"pk": credit_card.id})
        input = {
            "data": {
                "type": "credit-cards",
                "id": str(credit_card.id),
                "attributes": {
                    "number": factory.Faker("credit_card_number").generate(),
                    "franchise": random.choice(CreditCardFranchises.choices)[0],
                    "due_date_year": factory.Faker("random_int", min=2020, max=2030).generate(),
                    "due_date_month": factory.Faker("random_int", min=1, max=12).generate(),
                    "verification_code": factory.Faker("credit_card_security_code").generate(),
                    "is_principal": factory.Faker("boolean").generate(),
                },
                "relationships": {
                    "user": {"data": {"id": User.objects.order_by("?").first().id, "type": "users"}}
                },
            }
        }
        response = self.client.put(url, json.dumps(input), content_type="application/vnd.api+json")
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_patchCreditCardsForbidden(self):
        """
        Check edition forbidden
        """
        user = User.objects.create_user(email="superuser@example.com", is_superuser=True)
        self.client.force_authenticate(user=user)
        credit_card = CreditCard.objects.order_by("?").first()
        url = reverse("credit_card-detail", kwargs={"pk": credit_card.id})
        input = {
            "data": {
                "type": "provider-locations",
                "id": str(credit_card.id),
                "attributes": {
                    "number": factory.Faker("credit_card_number").generate(),
                },
            }
        }
        response = self.client.patch(
            url, json.dumps(input), content_type="application/vnd.api+json"
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_deleteCreditCards(self):
        """
        Check user deletion
        """
        # Super user
        ## Delete another user credit card
        user = User.objects.create_user(email="superuser@example.com", is_superuser=True)
        self.client.force_authenticate(user=user)
        credit_card = CreditCard.objects.filter(~Q(user=user.id)).order_by("?").first()
        url = reverse("credit_card-detail", kwargs={"pk": credit_card.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(CreditCard.objects.filter(id=user.id).exists())

        # Standard user
        user1 = User.objects.create_user(email="standarduser1@example.com")
        credit_card1 = CreditCardFactory(user=user1)
        user2 = User.objects.create_user(email="standarduser2@example.com")
        credit_card2 = CreditCardFactory(user=user2)
        self.client.force_authenticate(user=user1)

        ## Delete another user credit card
        url_fail = reverse("credit_card-detail", kwargs={"pk": credit_card2.id})
        response_fail = self.client.delete(url_fail)
        self.assertEqual(response_fail.status_code, status.HTTP_404_NOT_FOUND)

        ## Delete current user credit card
        url = reverse("credit_card-detail", kwargs={"pk": credit_card1.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(CreditCard.objects.filter(id=credit_card1.id).exists())

        # Anonymous user
        ## Delete any user
        credit_card = CreditCard.objects.order_by("?").first()
        url = reverse("credit_card-detail", kwargs={"pk": credit_card.id})
        self.client.force_authenticate(user=None)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
