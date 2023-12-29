from dataclasses import dataclass
from typing import Optional, Any


@dataclass
class TransactionData:
    source_wallet_id: int
    destination_wallet_id: int
    amount: int
    action_type: "ActionChoices.choices"
    description: str
    index: Optional[Any] = None
