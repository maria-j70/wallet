from django.test import TestCase
from django.utils import dateparse
from freezegun import freeze_time
from rest_framework.test import APIClient

from wallet import factories


class WalletTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.f_time_str = "2023-10-09T13:11:44.657109Z"
        cls.f_datetime = dateparse.parse_datetime(cls.f_time_str)

        with freeze_time(cls.f_time_str):
            cls.user_1 = factories.UserFactory.create()
            cls.user_2 = factories.UserFactory.create()

            cls.amount_1 = 100
            cls.amount_2 = 200

            cls.wallet_11 = factories.WalletFactory.create(owner=cls.user_1, balance=cls.amount_1)
            cls.wallet_12 = factories.WalletFactory.create(owner=cls.user_1, balance=cls.amount_2)

            cls.wallet_21 = factories.WalletFactory.create(owner=cls.user_2, balance=cls.amount_1)
            cls.wallet_22 = factories.WalletFactory.create(owner=cls.user_2, balance=cls.amount_2)

    def setUp(self):
        self.client = APIClient()

    def test_get_wallets(self):
        self.client.force_authenticate(user=WalletTests.user_1)

        expected_response = {
            "count": 2,
            "next": None,
            "previous": None,
            "results": sorted(
                [
                    {
                        "id": self.wallet_11.id,
                        "balance": self.amount_1,
                        "is_deleted": False,
                        "created_at": self.f_time_str,
                        "updated_at": self.f_time_str,
                    },
                    {
                        "id": self.wallet_12.id,
                        "balance": self.amount_2,
                        "is_deleted": False,
                        "created_at": self.f_time_str,
                        "updated_at": self.f_time_str,
                    },
                ],
                key=lambda o: o["id"],
            ),
        }

        response = self.client.get("/api/v1/wallets/")
        self.assertEqual(response.status_code, 200)
        response_dict = response.json()
        response_dict["results"].sort(key=lambda o: o["id"])
        self.maxDiff = None
        self.assertEqual(response.json(), expected_response)

    def test_creat_wallet(self):
        response = self.client.post("/api/v1/wallets/")
        self.assertEqual(response.status_code, 401)

        expected_response = {
            "balance": 0,
            "is_deleted": False,
            "created_at": self.f_time_str,
            "updated_at": self.f_time_str,
            "owner": {"id": self.user_1.id, "first_name": self.user_1.first_name, "last_name": self.user_1.last_name},
        }

        with freeze_time(self.f_time_str):
            self.client.force_authenticate(user=self.user_1)
            response = self.client.post("/api/v1/wallets/")

        self.assertEqual(response.status_code, 201)
        response_dict = response.json()
        self.assertIn("id", response_dict)
        response_dict.pop("id")
        self.maxDiff = None
        self.assertEqual(response.json(), expected_response)

    def test_detail_wallet(self):
        self.client.force_authenticate(user=self.user_1)
        response = self.client.get("/api/v1/wallets/{}".format(self.wallet_11.id))
        expected_response = {
            "id": self.wallet_11.id,
            "balance": self.amount_1,
            "is_deleted": False,
            "created_at": self.f_time_str,
            "updated_at": self.f_time_str,
            "owner": {"id": self.user_1.id, "first_name": self.user_1.first_name, "last_name": self.user_1.last_name},
        }

        self.assertEqual(response.status_code, 200)
        self.maxDiff = None
        self.assertEqual(response.json(), expected_response)
