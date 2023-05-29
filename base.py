import math
from typing import Self
from typing import Union
from typing import Optional

TOP = "1"
BOTTOM = "0"

Example = dict[str, bool]

class HornClause:
    def __init__(self, antecedent: list[str], consequent: str):
        self.antecedent = antecedent
        self.consequent = consequent

    def __str__(self):
        if len(self.antecedent) == 0:
            s = TOP
        else:
            s = "∧".join(sorted(list(self.antecedent)))
        return f"({s} → {BOTTOM if not self.consequent else self.consequent})"
    
    def evaluate(self, e: Example) -> bool:
        for a in self.antecedent:
            if not e[a]:
                return True
        if not self.consequent:
            return False
        else:
            return e[self.consequent]

class HornFormula:
    def __init__(self, clauses: list[HornClause]):
        self.clauses = clauses

    def __str__(self):
        f0 = map(str, self.clauses)
        return "∧".join(f0)

    def vars(self) -> list[str]:
        v = set()
        for c in self.clauses:
            v.update(c.antecedent)
            v.add(c.consequent)
        return sorted(list(v))

    def make_example(self, s: str) -> Example:
        vars = self.vars()
        assert(len(s) == len(vars))
        result = dict()
        for i, v in enumerate(vars):
            result[v] = s[i] == "1"
        return result

    def evaluate(self, e: Union[str, Example]) -> bool:
        if type(e) is str:
            e = self.make_example(e)
        for c in self.clauses:
            r = c.evaluate(e)
            if not r:
                return False
        return True

    # TODO: replace with proper implementation! (currently just brute-forces all possible assignments)
    def equivalent(self, f: Self) -> tuple[bool, Optional[Example]]:
        vars = self.vars()
        for i in range(math.floor(math.pow(2, len(vars)))):
            e = self.make_example(bin(i)[2:].zfill(len(vars)))

            if self.evaluate(e) != f.evaluate(e):
                return False, e
        return True, None

def true(e: Example) -> set[str]:
    r = set()
    for v in e.keys():
        if e[v]:
            r.add(v)
    return r

def false(e: Example) -> set[str]:
    r = set()
    for v in e.keys():
        if not e[v]:
            r.add(v)
    return r

def intersect(e1: Example, e2: Example) -> Example:
    assert(len(e1) == len(e2))
    r = dict()
    for v in e1.keys():
        r[v] = e1[v] and e2[v]
    return r

def covers(e: Example, c: HornClause) -> bool:
    return set(c.antecedent).issubset(true(e))

def violates(e: Example, c: HornClause) -> bool:
    if not covers(e, c):
        return False
    if c.consequent == "":
        return True
    else:
        return not e[c.consequent]
