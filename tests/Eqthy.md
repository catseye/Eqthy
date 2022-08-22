Eqthy
=====

This document provides a number of example Eqthy sources in
Falderal format, in the hopes that they will help clarify
the semantics of the language.
For an overview of the language, see the README file.

    -> Functionality "Check Eqthy source" is implemented by shell command
    -> "python3 bin/eqthy %(test-body-file)"

    -> Tests for functionality "Check Eqthy source"

This source consists of some axioms and a theorem.

    axiom mul(A, e) = A
    axiom mul(e, A) = A
    axiom mul(A, mul(B, C)) = mul(mul(A, B), C)
    theorem
        mul(A, e) = mul(e, A)
    proof
        A = A
        mul(A, e) = A
        mul(A, e) = mul(e, A)
    qed
    ===> ok
