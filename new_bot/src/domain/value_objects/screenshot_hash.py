from dataclasses import dataclass

@dataclass(frozen=True)
class ScreenshotHash:
    value: str

    def __post_init__(self):
        if not self.value:
            raise ValueError("Hash cannot be empty")
        # Normalize to lowercase allows flexible input, but usually hash is fixed format.
        # Immutability via frozen=True implies we can't change 'value' here easily unless we leverage object.__setattr__
        # or rely on constructor arguments being correct. 
        # For simplicity in frozen dataclass, we assume proper construction or validate.
        # However, to enforce normalization on init in a frozen dataclass requires simple trick or separate factory.
        # We will enforce validation here. Normalization should be done before creating if strict frozen.
        if self.value != self.value.lower():
             raise ValueError("Hash must be normalized (lowercase)")
