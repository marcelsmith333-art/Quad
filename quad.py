from enum import IntEnum
from dataclasses import dataclass, field
from typing import List, Dict
import hashlib

class BITE(IntEnum):
    PRESERVE=0; CREATE=1; MUTATE=2; REMOVE=3

@dataclass
class QUAD:
    bites: List[BITE]
    def hash(self): 
        return hashlib.sha256(",".join(str(b.value) for b in self.bites).encode()).hexdigest()[:16]

@dataclass
class BuildCreditLedger:
    supply: float=0.0
    balances: Dict[str,float]=field(default_factory=dict)
