from enum import Enum

class WithdrawalStatus(str, Enum):
    CREATED = "CREATED"
    COMPLETED = "COMPLETED"
    FAIL = "FAIL"
    UNKNOWN = "UNKNOWN"
    """Returned when xRocket API does not sent status"""