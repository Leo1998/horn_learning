import math

from typing import Self, Union, Optional

TOP = "1"
BOTTOM = "0"

Example = dict[str, bool]

# Methods for Examples

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

# Definitions for 'traditional' horn clauses

class HornClause:
    def __init__(self, antecedent: list[str], consequent: Optional[str]):
        self.antecedent = antecedent
        self.consequent = consequent

    def __str__(self):
        if len(self.antecedent) == 0:
            s = TOP
        else:
            s = "∧".join(sorted(list(self.antecedent)))
        return f"({s} → {BOTTOM if self.consequent is None else self.consequent})"
    
    def is_member(self, e: Example) -> bool:
        for a in self.antecedent:
            if not e[a]:
                return True
        if self.consequent is None:
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
            if c.consequent is not None:
                v.add(c.consequent)
        return sorted(list(v))

    def make_example(self, s: str) -> Example:
        vars = self.vars()
        assert(len(s) == len(vars))
        result = dict()
        for i, v in enumerate(vars):
            result[v] = s[i] == "1"
        return result

    def is_member(self, e: Union[str, Example]) -> bool:
        if type(e) is str:
            e = self.make_example(e)
        for c in self.clauses:
            r = c.is_member(e)
            if not r:
                return False
        return True

    # TODO: replace with proper implementation! (currently just brute-forces all possible assignments)
    def is_equivalent(self, f: Self) -> tuple[bool, Optional[Example]]:
        vars = self.vars()
        for i in reversed(range(math.floor(math.pow(2, len(vars))))):
            e = self.make_example(bin(i)[2:].zfill(len(vars))) # hacky way to generate all possibilities

            if self.is_member(e) != f.is_member(e):
                return False, e
        return True, None

def covers(e: Example, c: HornClause) -> bool:
    return set(c.antecedent).issubset(true(e))

def violates(e: Example, c: HornClause) -> bool:
    if not covers(e, c):
        return False
    if c.consequent is None:
        return True
    else:
        return not e[c.consequent]

def gen_clauses(examples: list[Example]) -> list[HornClause]:
    clauses = []
    for e in examples:
        t = list(true(e))
        for f in false(e):
            clauses.append(HornClause(t, f))
        clauses.append(HornClause(t, None))
    return clauses

# Definitions for 'meta' horn clauses

class HornMetaClause:
    def __init__(self, antecedent: list[str], consequent: list[str]):
        self.antecedent = antecedent
        self.consequent = consequent

    def __str__(self):
        if len(self.antecedent) == 0:
            a = TOP
        else:
            a = "∧".join(sorted(list(self.antecedent)))
        if len(self.consequent) == 0:
            c = BOTTOM
        else:
            c = "∧".join(sorted(list(self.consequent)))
        return f"({a} → {c})"
    
    def is_member(self, e: Example) -> bool:
        for a in self.antecedent:
            if not e[a]:
                return True
        if len(self.consequent) == 0:
            return False
        for c in self.consequent:
            if not e[c]:
                return False
        return True

class HornMetaFormula:
    def __init__(self, clauses: list[HornMetaClause]):
        self.clauses = clauses

    def __str__(self):
        f0 = map(str, self.clauses)
        return "∧".join(f0)

    def vars(self) -> list[str]:
        v = set()
        for c in self.clauses:
            v.update(c.antecedent)
            v.update(c.consequent)
        return sorted(list(v))

    def make_example(self, s: str) -> Example:
        vars = self.vars()
        assert(len(s) == len(vars))
        result = dict()
        for i, v in enumerate(vars):
            result[v] = s[i] == "1"
        return result

    def is_member(self, e: Union[str, Example]) -> bool:
        if type(e) is str:
            e = self.make_example(e)
        for c in self.clauses:
            r = c.is_member(e)
            if not r:
                return False
        return True

    # TODO: replace with proper implementation! (currently just brute-forces all possible assignments)
    def is_equivalent(self, f: Self) -> tuple[bool, Optional[Example]]:
        vars = self.vars()
        for i in reversed(range(math.floor(math.pow(2, len(vars))))):
            e = self.make_example(bin(i)[2:].zfill(len(vars))) # hacky way to generate all possibilities

            if self.is_member(e) != f.is_member(e):
                return False, e
        return True, None

def covers_meta(e: Example, c: HornMetaClause) -> bool:
    return set(c.antecedent).issubset(true(e))

def violates_meta(e: Example, c: HornMetaClause) -> bool:
    if not covers(e, c):
        return False
    if len(c.consequent) == 0:
        return True
    else:
        for s in c.consequent:
            if not e[s]:
                return True
        return False

def negex_meta(c: HornMetaClause, vars: list[str]) -> Example:
    result = dict()
    for v in vars:
        result[v] = v in c.antecedent
    return result

def new_meta(e: Example) -> HornMetaClause:
    return HornMetaClause(true(e), [])

def reduce_meta(e: Example, c: HornMetaClause, negexC: Example) -> bool:
    if len(c.consequent) == 0:
        c.consequent = true(e).intersection(false(negexC))
    else:
        c.consequent = true(e).intersection(c.consequent)

def refine_meta(e: Example, c: HornMetaClause, negexC: Example) -> bool:
    consequent = []
    if len(c.consequent) > 0:
        consequent.extend(c.consequent)
        consequent.extend(false(e).intersection(true(negexC)))
    c.antecedent = true(e)
    c.consequent = consequent