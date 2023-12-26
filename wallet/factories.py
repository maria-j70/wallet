from django.contrib.auth import get_user_model

from user_config.models import Config
from wallet_app.models import Wallet
import factory
from factory.django import DjangoModelFactory
from transaction.models import Transaction

User = get_user_model()


class ConfigFactory(DjangoModelFactory):
    class Meta:
        model = Config
    wage_rate = 0.01
    default = True
    min = 1000
    max = 10000


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.sequence(lambda n: "user_{}".format(n))
    first_name = "John"
    last_name = "Doe"
    email = factory.sequence(lambda n: "test{}@example.com".format(n))
    password = "password"
    config = factory.SubFactory(ConfigFactory)


class WalletFactory(DjangoModelFactory):
    class Meta:
        model = Wallet

    owner = factory.SubFactory(UserFactory)
    balance = 100


class TransactionsFactory(DjangoModelFactory):
    class Meta:
        model = Transaction

    tracker_id = factory.sequence(lambda n: n)


