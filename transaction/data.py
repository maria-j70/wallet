from dataclasses import dataclass
from typing import Optional, Any


@dataclass
class TransactionData:
    source_wallet: "Wallet"
    destination_wallet: "Wallet"
    amount: int
    action_type: "ActionChoices.choices"
    description: str
    index: Optional[Any] = None
