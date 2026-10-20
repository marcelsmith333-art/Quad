from enum import IntEnum
from dataclasses import dataclass, field
from typing import List, Dict
import hashlib

class BITE(IntEnum):
    PRESERVE=0; CREATE=1; MUTATE=2; REMOVE=3

@dataclass
class QUAD:
    bites: List[BITE]
    def __post_init__(self):
        self.bites=[b if isinstance(b, BITE) else BITE(b) for b in self.bites]
    def hash(self): 
        return hashlib.sha256(",".join(str(b.value) for b in self.bites).encode()).hexdigest()[:16]

@dataclass
class BuildCreditLedger:
    supply: float=0.0
    balances: Dict[str,float]=field(default_factory=dict)
    def submit(self, quad: QUAD, owner="Marcel Smith"):
        mint = 2.0 if len(set(quad.bites)) == 1 else 8.0
        self.supply += mint
        self.balances[owner] = self.balances.get(owner, 0) + mint
        print(f"SUBMIT {[int(b) for b in quad.bites]} -> Mint {int(mint)} Supply {self.supply}")
        return mint

ledger = BuildCreditLedger()
quads = [[1,1,1,1],[0,0,0,0],[2,2,2,2],[3,0,2,1]]
for q in quads:
    ledger.submit(QUAD([BITE(x) for x in q]))

print("BURN -0.5 on REMOVE")
print(f"FINAL Supply: {ledger.supply} Build Credits")