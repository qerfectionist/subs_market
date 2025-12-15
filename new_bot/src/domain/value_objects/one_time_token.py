from dataclasses import dataclass

@dataclass(frozen=True)
class OneTimeToken:
    value: str

    def __post_init__(self):
        if not self.value:
            raise ValueError("Token cannot be empty")
