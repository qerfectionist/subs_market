from dataclasses import dataclass

@dataclass(frozen=True)
class BillingMonth:
    year: int
    month: int

    def __post_init__(self):
        if not (1 <= self.month <= 12):
            raise ValueError("Month must be between 1 and 12")
    def next(self) -> "BillingMonth":
        if self.month == 12:
            return BillingMonth(year=self.year + 1, month=1)
        return BillingMonth(year=self.year, month=self.month + 1)

    @staticmethod
    def current() -> "BillingMonth":
        from datetime import date
        today = date.today()
        return BillingMonth(year=today.year, month=today.month)
