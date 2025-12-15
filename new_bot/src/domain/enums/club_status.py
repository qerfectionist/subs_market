from enum import Enum

class ClubStatus(str, Enum):
    RECRUITING = "recruiting"
    ACTIVE = "active"
    PAUSED = "paused"
    CLOSED = "closed"
