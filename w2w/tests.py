from django.utils import dateparse
from freezegun import freeze_time
from rest_framework.test import APITestCase

from transaction.models import ActionChoices, Transaction
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

            cls.balance_1 = 100
            cls.balance_2 = 200

            cls.wallet_11 = WalletFactory.create(owner=cls.user_1, balance=cls.balance_1)
            cls.wallet_12 = WalletFactory.create(owner=cls.user_1, balance=cls.balance_2)

            cls.wallet_21 = WalletFactory.create(owner=cls.user_2, balance=cls.balance_1)
            cls.wallet_22 = WalletFactory.create(owner=cls.user_2, balance=cls.balance_2)

    def test_simple_success_w2w(self):
        self.client.force_authenticate(user=self.user_1)
        transfer_amount = 30
        init_source_balance = self.wallet_11.balance
        init_destination_balance = self.wallet_21.balance

        with freeze_time(self.f_time_str):
            response = self.client.post('/api/v1/w2w/', {
                "source_wallet": self.wallet_11.id,
                "destination_wallet": self.wallet_21.id,
                "tracker_id": "123",
                "amount": transfer_amount
            })
            self.assertEqual(response.status_code, 200)

        expected_response = {
            'created_at': '2023-10-09T13:11:44.657109Z',
            'actions': sorted([
                {
                    'wallet': {
                        'id': self.wallet_11.id,
                        'balance': init_source_balance - transfer_amount,
                        'is_deleted': False,
                        'created_at': '2023-10-09T13:11:44.657109Z',
                        'updated_at': '2023-10-09T13:11:44.657109Z',
                        'owner': {
                            'id': self.user_1.id,
                            'first_name': self.user_1.first_name,
                            'last_name': self.user_1.last_name
                        }
                    },
                    'amount': -transfer_amount,
                    'type': ActionChoices.withdrew.value,
                    'description': f'Transfer money from {self.user_1.username} to {self.user_2.username} wallets',
                    'created_at': '2023-10-09T13:11:44.657109Z'
                }, {
                    'wallet': {
                        'id': self.wallet_21.id,
                        'balance': init_destination_balance + transfer_amount,
                        'is_deleted': False,
                        'created_at': '2023-10-09T13:11:44.657109Z',
                        'updated_at': '2023-10-09T13:11:44.657109Z',
                        'owner': {
                            'id': self.user_2.id,
                            'first_name': self.user_2.first_name,
                            'last_name': self.user_2.last_name
                        }
                    },
                    'amount': transfer_amount,
                    'type': ActionChoices.deposit.value,
                    'description': f'Transfer money from {self.user_1.username} to {self.user_2.username} wallets',
                    'created_at': '2023-10-09T13:11:44.657109Z'
                }], key=lambda o: o["wallet"]['id'])
        }
        response_dict = response.json()

        self.assertIn("id", response_dict)
        transaction_id = response_dict.pop('id')
        w2w_obj = Transaction.objects.get(id=transaction_id).content_object
        self.assertEqual(w2w_obj.status , FeaturesStatus.done)
        self.assertEqual(w2w_obj.source_wallet_id, self.wallet_11.id)
        self.assertEqual(w2w_obj.destination_wallet_id, self.wallet_21.id)
        self.assertEqual(w2w_obj.created_by_id , self.user_1.id)
        self.assertIn("actions", response_dict)
        self.assertIsInstance(response_dict["actions"], list)
        self.assertEqual(len(response_dict["actions"]), 2)
        self.assertIsInstance(response_dict["actions"][0], dict)
        self.assertIsInstance(response_dict["actions"][1], dict)
        self.assertIn("id", response_dict["actions"][0])
        self.assertIn("id", response_dict["actions"][1])
        response_dict["actions"][0].pop("id")
        response_dict["actions"][1].pop("id")
        self.maxDiff = None
        response_dict["actions"] = sorted(response_dict['actions'], key= lambda o:o["wallet"]['id'])
        self.assertEqual(response_dict, expected_response)
