#!/usr/bin/env python3

import itertools

from base import HornMetaClause, HornMetaFormula, Example, true, false, intersect, covers_meta, violates_meta, negex_meta, new_meta, reduce_meta, refine_meta

def horn1(target: HornMetaFormula) -> HornMetaFormula:
    H = HornMetaFormula([])
    while(True):
        equal, counter = target.is_equivalent(H)
        print(f"Current hypothesis: {H}")
        if equal:
            print("Success!!!")
            return H
        else:
            if not H.is_member(counter): # is a positive counterexample
                print(f"Positive counterexample: {counter}")
                for c in H.clauses:
                    if violates_meta(counter, c):
                        reduce_meta(counter, c, negex_meta(c, target.vars()))
                print("Eliminating incorrect clauses...")
            else: # is a negative counterexample
                print(f"Negative counterexample: {counter}")
                refined = False
                for c in H.clauses:
                    negex = negex_meta(c, target.vars())
                    intersected = intersect(negex, counter)
                    if true(intersected).issubset(true(negex)):
                        if not target.is_member(intersected):
                            print("Refining...")
                            refine_meta(intersected, c, negex) # refine with the intersection
                            refined = True
                            break
                if not refined:
                    print("Adding...")
                    H.clauses.append(new_meta(counter))
            print("") # newline


if __name__ == "__main__":
    testClause1 = HornMetaClause(["a", "c"], ["d"])
    testClause2 = HornMetaClause(["a", "b"], ["c"])
    testFormula = HornMetaFormula([testClause1, testClause2])

    print(f"Target formula: {testFormula}\n")

    horn1(testFormula)

    #print(testFormula.is_member("1110"))
    #print(testFormula.is_equivalent(HornMetaFormula([testClause1])))