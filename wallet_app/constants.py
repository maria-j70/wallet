import logging

from django.conf import settings

from utils.internal_exceptions import SystemWalletNotExistsError

logger = logging.getLogger(__name__)

SYSTEM_WALLET_USERNAME = "system"


class InternalWallets:
    _SYSTEM = None

    @classmethod
    def _load_system_wallet(cls):
        from wallet_app.models import Wallet
        SYSTEM_WALLET = Wallet.objects.filter(owner__username="system").first()
        if not SYSTEM_WALLET:
            logger.critical(msg="The system wallet not exists! create it immediately!")
        return SYSTEM_WALLET

    @classmethod
    @property
    def SYSTEM(cls):  # NoQA
        if cls._SYSTEM and settings.PHASE != settings.PhaseChoices.TEST:
            return cls._SYSTEM
        system_wallet = cls._load_system_wallet()
        if not system_wallet:
            raise SystemWalletNotExistsError
        cls._SYSTEM = system_wallet
        return cls._SYSTEM
