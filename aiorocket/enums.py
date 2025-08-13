from enum import Enum

__all__ = [
    'WithdrawalStatus',
    'Network'
]

class WithdrawalStatus(str, Enum):
    CREATED = "CREATED"
    COMPLETED = "COMPLETED"
    FAIL = "FAIL"
    
    UNKNOWN = "UNKNOWN"
    """Returned when xRocket API does not sent status"""
    
class Network(str, Enum):
    TON = "TON"
    BSC = "BSC"
    ETH = "ETH"
    BTC = "BTC"
    TRX = "TRX"
    SOL = "SOL"
    
    UNKNOWN = "UNKNOWN"
    """Returned when xRocket API does not sent network"""