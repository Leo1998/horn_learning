#!/usr/bin/env python3

import itertools

from base import HornClause, HornFormula, Example, true, false, intersect, covers, violates, gen_clauses

def horn(target: HornFormula) -> HornFormula:
    S = []
    H = HornFormula([])
    while(True):
        equal, counter = target.is_equivalent(H)
        print(f"Current hypothesis: {H}")
        if equal:
            print("Success!!!")
            return H
        else:
            if not H.is_member(counter): # is a positive counterexample
                print(f"Positive counterexample: {counter}")
                H.clauses = list(itertools.filterfalse(lambda c: violates(counter, c), H.clauses)) # remove from H every clause that x violates
                print("Eliminating incorrect clauses...")
            else: # is a negative counterexample
                print(f"Negative counterexample: {counter}")
                refined = False
                for i, s in enumerate(S):
                    intersected = intersect(s, counter)
                    if true(intersected).issubset(true(s)):
                        if not target.is_member(intersected):
                            print("Refining...")
                            S[i] = intersected # refine with the intersection
                            refined = True
                if not refined:
                    print("Adding...")
                    S.append(counter)
                H.clauses = gen_clauses(S) # regenerate H


if __name__ == "__main__":
    testClause1 = HornClause(["a", "c"], "d")
    testClause2 = HornClause(["a", "b"], "c")
    testFormula = HornFormula([testClause1, testClause2])

    print(f"Target formula: {testFormula}")

    print(f"Horn algorithm result: {horn(testFormula)}")

    #print(testFormula.evaluate("1110"))
    #print(testFormula.equivalent(HornFormula([testClause1])))