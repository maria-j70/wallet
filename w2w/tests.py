from django.utils import dateparse
from freezegun import freeze_time
from rest_framework.test import APITestCase

from transaction.models import Transaction
from utils.base_moldel import FeaturesStatus
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
            cls.system_user = UserFactory.create(username='system')

            cls.balance_1 = 100000
            cls.balance_2 = 200000

            cls.wallet_11 = WalletFactory.create(owner=cls.user_1, balance=cls.balance_1)
            cls.wallet_12 = WalletFactory.create(owner=cls.user_1, balance=cls.balance_2)

            cls.wallet_21 = WalletFactory.create(owner=cls.user_2, balance=cls.balance_1)
            cls.wallet_22 = WalletFactory.create(owner=cls.user_2, balance=cls.balance_2)
            cls.system_wallet = WalletFactory.create(owner=cls.system_user, balance=1000000)

    def test_simple_success_w2w(self):
        self.client.force_authenticate(user=self.user_1)
        transfer_amount = 30000
        init_source_balance = self.wallet_11.balance
        init_destination_balance = self.wallet_21.balance

        with freeze_time(self.f_time_str):
            response = self.client.post(
                "/api/v1/w2w/",
                {
                    "source_wallet": self.wallet_11.id,
                    "destination_wallet": self.wallet_21.id,
                    "tracker_id": "123",
                    "amount": transfer_amount,
                },
            )
            self.assertEqual(response.status_code, 200, msg=response.json())

        expected_response = {
            'created_at': '2023-10-09T13:11:44.657109Z',
            'actions': sorted(
                [{
                    'wallet': self.system_wallet.id,
                    'amount': 1000,
                    'action_type': 3,
                    'description': f'transfer money from wallet with ID {self.wallet_11.id} to wallet with ID system for wage',
                    'created_at': '2023-10-09T13:11:44.657109Z'
                }, {
                    'wallet': self.wallet_11.id,
                    'amount': -1000,
                    'action_type': 3,
                    'description': f'transfer money from wallet with ID {self.wallet_11.id} to wallet with ID'
                                   f' system for wage',
                    'created_at': '2023-10-09T13:11:44.657109Z'
                }, {
                    'wallet': self.wallet_21.id,
                    'amount': 30000,
                    'action_type': 0,
                    'description': f'transfer money from wallet with ID {self.wallet_11.id} to wallet with '
                                   f'ID {self.wallet_21.id}',
                    'created_at': '2023-10-09T13:11:44.657109Z'
                }, {
                    'wallet': self.wallet_11.id,
                    'amount': -30000,
                    'action_type': 0,
                    'description': f'transfer money from wallet with ID {self.wallet_11.id} to wallet with '
                                   f'ID {self.wallet_21.id}',
                    'created_at': '2023-10-09T13:11:44.657109Z'
                }], key=lambda o: o["wallet"])
        }

        response_dict = response.json()

        self.assertIn("id", response_dict)
        transaction_id = response_dict.pop("id")
        w2w_obj = Transaction.objects.get(id=transaction_id).content_object
        self.assertEqual(w2w_obj.status, FeaturesStatus.done)
        self.assertEqual(w2w_obj.source_wallet_id, self.wallet_11.id)
        self.assertEqual(w2w_obj.destination_wallet_id, self.wallet_21.id)
        self.assertEqual(w2w_obj.created_by_id, self.user_1.id)
        self.assertIn("actions", response_dict)
        self.assertIsInstance(response_dict["actions"], list)

        self.assertEqual(len(response_dict["actions"]), 4)
        for i in range(4):
            self.assertIsInstance(response_dict["actions"][i], dict)
            self.assertIn("id", response_dict["actions"][i])
            response_dict["actions"][i].pop("id")

        self.maxDiff = None
        response_dict["actions"] = sorted(response_dict["actions"], key=lambda o: o["wallet"])
        self.assertEqual(response_dict, expected_response)
