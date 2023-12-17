from django.utils import dateparse
from freezegun import freeze_time
from rest_framework.test import APITestCase

from wallet.factories import UserFactory, WalletFactory


class W2WAPITests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.f_time_str = "2023-10-09T13:11:44.657109Z"
        cls.f_datetime = dateparse.parse_datetime(cls.f_time_str)

        with freeze_time(cls.f_time_str):
            cls.user_1 = UserFactory.create()
            cls.user_2 = UserFactory.create()

            cls.balance_1 = 100
            cls.balance_2 = 200

            cls.wallet_11 = WalletFactory.create(owner=cls.user_1, balance=cls.balance_1)
            cls.wallet_12 = WalletFactory.create(owner=cls.user_1, balance=cls.balance_2)

            cls.wallet_21 = WalletFactory.create(owner=cls.user_2, balance=cls.balance_1)
            cls.wallet_22 = WalletFactory.create(owner=cls.user_2, balance=cls.balance_2)

    def test_simple_success_deposit(self):
        self.client.force_authenticate(user=self.user_1)
        deposit_amount = 1000
        init_source_balance = self.wallet_11.balance

        with freeze_time(self.f_time_str):
            response = self.client.post('/api/v1/deposit/', {
                "tracker_id": "123",
                "amount": deposit_amount,
                "wallet": self.wallet_11.id
            })
        self.assertEqual(response.status_code, 201)
        pass

        expected_response = {
            'created_at': '2023-10-09T13:11:44.657109Z',
            'tracker_id': '123',
            'amount': deposit_amount,
            'wallet': self.wallet_11.id
        }
        response_dict = response.json()

        self.assertIn("id", response_dict)
        response_dict.pop('id')
        self.maxDiff = None
        self.assertEqual(response_dict, expected_response)
