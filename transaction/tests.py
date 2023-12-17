# from django.test import TestCase
# from rest_framework.test import APIClient
# from wallet.factories import UserFactory, WalletFactory, TransactionsFactory
# from freezegun import freeze_time
#
#
# # Create your tests here.
#
# class TransactionTests(TestCase):
#
#     @classmethod
#     def setUpTestData(cls):
#         super().setUpTestData()
#
#     @classmethod
#     def setUpClass(cls):
#         super().setUpClass()
#         cls.f_time_str = "2023-10-09T13:11:44.657109Z"
#
#         with freeze_time(cls.f_time_str):
#             cls.user_1 = UserFactory.create()
#             cls.user_2 = UserFactory.create()
#
#             cls.amount_1 = 100
#             cls.amount_2 = 200
#
#             cls.wallet_11 = WalletFactory.create(owner=cls.user_1, balance=cls.amount_1)
#             cls.wallet_12 = WalletFactory.create(owner=cls.user_1, balance=cls.amount_2)
#
#             cls.wallet_21 = WalletFactory.create(owner=cls.user_2, balance=cls.amount_1)
#             cls.wallet_22 = WalletFactory.create(owner=cls.user_2, balance=cls.amount_2)
#
#     def setUp(self):
#         self.client = APIClient()
#
#     def test_create_transaction(self):
#         self.client.force_authenticate(user=TransactionTests.user_1)
#         with freeze_time(TransactionTests.f_time_str):
#             response_1 = self.client.post('/api/v1/transaction/', {"source": TransactionTests.wallet_11.id,
#                                                                    "destination": TransactionTests.wallet_22.id,
#                                                                    "tracker_id": 1,
#                                                                    "amount": 10
#                                                                    })
#
#             expected_response_1 = {'id': 1,
#                                    'created_at': '2023-10-09T13:11:44.657109Z',
#                                    'tracker_id': '1',
#                                    'actions':
#                                        [{'id': 1, 'wallet': {'id': 1, 'balance': 90, 'is_deleted': False,
#                                                              'created_at': '2023-10-09T13:11:44.657109Z',
#                                                              'updated_at': '2023-10-09T13:11:44.657109Z',
#                                                              'owner': {'id': 1, 'username': 'user_0',
#                                                                        'first_name': 'John', 'last_name': 'Doe',
#                                                                        'email': 'test0@example.com'}}, 'amount': -10,
#                                          'type': 1, 'description': 'Transfer money from user_0 to user_1 wallets',
#                                          'created_at': '2023-10-09T13:11:44.657109Z'},
#                                         {'id': 2, 'wallet': {'id': 4, 'balance': 210, 'is_deleted': False,
#                                                              'created_at': '2023-10-09T13:11:44.657109Z',
#                                                              'updated_at': '2023-10-09T13:11:44.657109Z',
#                                                              'owner': {'id': 2, 'username': 'user_1',
#                                                                        'first_name': 'John', 'last_name': 'Doe',
#                                                                        'email': 'test1@example.com'}}, 'amount': 10,
#                                          'type': 0, 'description': 'Transfer money from user_0 to user_1 wallets',
#                                          'created_at': '2023-10-09T13:11:44.657109Z'}]}
#             self.assertEqual(response_1.status_code, 200)
#             self.maxDiff = None
#             self.assertEqual(response_1.json(), expected_response_1)
#
#             response_2 = self.client.post('/api/v1/transaction/', {"source": TransactionTests.wallet_22.id,
#                                                                    "destination": TransactionTests.wallet_11.id,
#                                                                    "tracker_id": 1,
#                                                                    "amount": 10
#                                                                    })
#             self.assertEqual(response_2.status_code, 404)
#
#     def test_history(self):
#         expected_response = {'count': 2,
#                              'next': None,
#                              'previous': None,
#                              'results': [{'id': 1, 'wallet': {'id': 1, 'balance': 110, 'is_deleted': False,
#                                                               'created_at': '2023-10-09T13:11:44.657109Z',
#                                                               'updated_at': '2023-10-09T13:11:44.657109Z',
#                                                               'owner': {'id': 1, 'username': 'user_0',
#                                                                         'first_name': 'John', 'last_name': 'Doe',
#                                                                         'email': 'test0@example.com'}}, 'amount': -10,
#                                           'type': 1, 'description': 'Transfer money from user_0 to user_1 wallets',
#                                           'created_at': '2023-10-09T13:11:44.657109Z'},
#                                          {'id': 4, 'wallet': {'id': 1,
#                                                               'balance': 110,
#                                                               'is_deleted': False,
#                                                               'created_at': '2023-10-09T13:11:44.657109Z',
#                                                               'updated_at': '2023-10-09T13:11:44.657109Z',
#                                                               'owner': {
#                                                                   'id': 1,
#                                                                   'username': 'user_0',
#                                                                   'first_name': 'John',
#                                                                   'last_name': 'Doe',
#                                                                   'email': 'test0@example.com'}},
#                                           'amount': 20, 'type': 0,
#                                           'description': 'Transfer money from user_1 to user_0 wallets',
#                                           'created_at': '2023-10-09T13:11:44.657109Z'}]}
#         with freeze_time(TransactionTests.f_time_str):
#             self.client.force_authenticate(user=TransactionTests.user_1)
#             self.client.post('/api/v1/transaction/', {"source": TransactionTests.wallet_11.id,
#                                                       "destination": TransactionTests.wallet_22.id,
#                                                       "tracker_id": 1,
#                                                       "amount": 10
#                                                       })
#             self.client.force_authenticate(user=TransactionTests.user_2)
#             self.client.post('/api/v1/transaction/', {"source": TransactionTests.wallet_21.id,
#                                                       "destination": TransactionTests.wallet_11.id,
#                                                       "tracker_id": 2,
#                                                       "amount": 20
#                                                       })
#
#             self.client.force_authenticate(user=TransactionTests.user_1)
#             response = self.client.get('/api/v1/transaction/history/{}'.format(TransactionTests.wallet_11.id))
#             self.assertEqual(response.status_code, 200)
#             self.maxDiff = None
#             self.assertEqual(response.json(), expected_response)
#
#     def test_deposit(self):
#         # normal deposit
#         self.client.force_authenticate(user=TransactionTests.user_1)
#         expected_response = {'id': 1,
#                              'created_at': TransactionTests.f_time_str,
#                              'tracker_id': '3',
#                              'amount': 100}
#         with freeze_time(TransactionTests.f_time_str):
#             response = self.client.post('/api/v1/transaction/deposit/{}'.format(TransactionTests.wallet_11.id),
#                                         {'tracker_id': '3', 'amount': 100})
#
#         self.assertEqual(response.status_code, 201)
#         self.maxDiff = None
#         self.assertEqual(response.json(), expected_response)
#
#         # try deposit to anybody else wallet
#         try:
#             self.client.post('/api/v1/transaction/deposit/{}'.format(TransactionTests.wallet_21.id),
#                              {'tracker_id': '4', 'amount': 100})
#         except Exception as e:
#             self.assertEqual(e.__str__(), "Wallet matching query does not exist.")
#
#         # try deposit to negative amount
#         expected_response = {'amount': ['Ensure this value is greater than or equal to 1.']}
#         response = self.client.post('/api/v1/transaction/deposit/{}'.format(TransactionTests.wallet_11.id),
#                                     {'tracker_id': '4', 'amount': -100})
#         self.assertEqual(response.status_code, 400)
#         self.maxDiff = None
#         self.assertEqual(response.json(), expected_response)
#
#     def test_withdrew(self):
#         # normal withdrew
#         self.client.force_authenticate(user=TransactionTests.user_1)
#         expected_response = {'id': 1,
#                              'created_at': TransactionTests.f_time_str,
#                              'tracker_id': '1',
#                              'amount': 10}
#         with freeze_time(TransactionTests.f_time_str):
#             response = self.client.post('/api/v1/transaction/withdrew/{}'.format(TransactionTests.wallet_11.id),
#                                         {'tracker_id': '1', 'amount': 10})
#
#         self.assertEqual(response.status_code, 201)
#         self.maxDiff = None
#         self.assertEqual(response.json(), expected_response)
#
#         # try withdrew to anybody else wallet
#         try:
#             self.client.post('/api/v1/transaction/withdrew/{}'.format(TransactionTests.wallet_21.id),
#                              {'tracker_id': '4', 'amount': 100})
#         except Exception as e:
#             self.assertEqual(e.__str__(), "Wallet matching query does not exist.")
#
#         # try withdrew to negative amount
#         expected_response = {'amount': ['Ensure this value is greater than or equal to 1.']}
#         response = self.client.post('/api/v1/transaction/withdrew/{}'.format(TransactionTests.wallet_11.id),
#                                     {'tracker_id': '4', 'amount': -100})
#         self.assertEqual(response.status_code, 400)
#         self.maxDiff = None
#         self.assertEqual(response.json(), expected_response)
#
