from enum import IntEnum
from dataclasses import dataclass, field
from typing import List, Dict
import hashlib

class BITE(IntEnum):
    PRESERVE=0; CREATE=1; MUTATE=2; REMOVE=3
    def intent_name(self):
        return {0:"PRESERVE",1:"CREATE",2:"MUTATE",3:"REMOVE"}[self.value]

@dataclass
class QUAD:
    bites: List[BITE]
    def __post_init__(self):
        self.bites=[b if isinstance(b, BITE) else BITE(b) for b in self.bites]
    def to_intent_code(self):
        c=0
        for b in self.bites: c=c*4+b.value
        return c
    def intent_string(self): 
        return "+".join(b.intent_name() for b in self.bites)
    def hash(self): 
        return hashlib.sha256(",".join(str(b.value) for b in self.bites).encode()).hexdigest()[:16]

@dataclass
class BuildCreditLedger:
    supply: float=0.0
    balances: Dict[str,float]=field(default_factory=dict)
    def submit(self, quad: QUAD, owner="Marcel Smith"):
        if len(set(quad.bites)) == 1:
            mint = 2.0
        else:
            mint = 8.0
        self.supply += mint
        self.balances[owner] = self.balances.get(owner, 0) + mint
        print(f"SUBMIT {[int(b) for b in quad.bites]} -> Mint {int(mint)} Supply {self.supply}")
        return mint

# --- GENESIS - Block 0 ---
ledger = BuildCreditLedger()
quads = [
    [1,1,1,1],  # CREATE x4
    [0,0,0,0],  # PRESERVE x4
    [2,2,2,2],  # MUTATE x4
    [3,0,2,1],  # REMOVE+PRESERVE+MUTATE+CREATE
]

print("--- Genesis Minting - Block 0 ---")
for q in quads:
    quad = QUAD([BITE(x) for x in q])
    ledger.submit(quad)

print("BURN -0.5 on REMOVE")
print(f"FINAL Supply: {ledger.supply} Build Credits")
print(f"Owner: Marcel Smith - 100% Sole Owner")
print(f"Block Hash Example: {quads[0]} -> {QUAD([BITE(x) for x in quads[0]]).hash()}")