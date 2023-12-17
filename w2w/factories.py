# from django.contrib.auth import get_user_model
# from wallet_app.models import Wallet
# import factory
# from factory.django import DjangoModelFactory
# from transaction.models import Transaction, Action, DepositToWallet, WithdrewToWallet
#
# User = get_user_model()
#
#
# class W2WFactory(DjangoModelFactory):
#     class Meta:
#         model = User
#
#     username = factory.sequence(lambda n: 'user_{}'.format(n))
#     first_name = 'John'
#     last_name = 'Doe'
#     email = factory.sequence(lambda n: 'test{}@example.com'.format(n))
#     password = "password"
