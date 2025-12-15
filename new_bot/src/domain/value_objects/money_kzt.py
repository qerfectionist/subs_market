from dataclasses import dataclass

@dataclass(frozen=True)
class MoneyKZT:
    amount: int

    def __post_init__(self):
        if self.amount < 0:
            raise ValueError("Amount cannot be negative")
