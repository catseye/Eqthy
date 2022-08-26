Eqthy
=====

This document provides a number of example Eqthy sources in
Falderal format, in the hopes that they will help clarify
the semantics of the language.
For an overview of the language, see the README file.

    -> Functionality "Parse Eqthy source" is implemented by shell command
    -> "python3 bin/eqthy --dump-ast %(test-body-file)"

    -> Tests for functionality "Parse Eqthy source"

This source is well-formed.  It will parse.

    axiom inv(A) = A
    ===> Program(axioms=[Axiom(name=None, eqn=Eqn(lhs=Term(ctor='inv', subterms=[Variable(name='A')]), rhs=Variable(name='A')))], theorems=[])

This source is not well-formed.  It will not parse.

    axiom inv(A) .
    ???> Expected '=', but found '.'

    -> Functionality "Check Eqthy source" is implemented by shell command
    -> "python3 bin/eqthy %(test-body-file) && echo 'ok'"

    -> Tests for functionality "Check Eqthy source"

This source consists of some axioms and a theorem.

    axiom mul(A, e) = A
    axiom mul(e, A) = A
    axiom mul(A, mul(B, C)) = mul(mul(A, B), C)
    theorem
        mul(A, e) = A
    proof
        A = A
        mul(A, e) = A
    qed
    ===> ok

Any variable name you like can be used in a theorem.

    axiom mul(A, e) = A
    axiom mul(e, A) = A
    axiom mul(A, mul(B, C)) = mul(mul(A, B), C)
    theorem
        mul(Z, e) = Z
    proof
        Z = Z
        mul(Z, e) = Z
    qed
    ===> ok

This "proof" contains a misstep.

    axiom mul(A, e) = A
    axiom mul(e, A) = A
    axiom mul(A, mul(B, C)) = mul(mul(A, B), C)
    theorem
        mul(A, e) = mul(foo, mul(e, A))
    proof
        A = A
        mul(A, e) = A
        mul(A, e) = mul(foo, mul(e, A))
    qed
    ???> DerivationError: Could not derive mul(A, e) = mul(foo, mul(e, A)) from mul(A, e) = A

This theorem does not prove what it says it proves.

    axiom mul(A, e) = A
    axiom mul(e, A) = A
    axiom mul(A, mul(B, C)) = mul(mul(A, B), C)
    theorem
        mul(A, e) = mul(A, A)
    proof
        A = A
        mul(A, e) = A
    qed
    ???> DerivationError: No step in proof showed mul(A, e) = mul(A, A)

This proof requires rewrites on the right-hand side of the equation.

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

Axioms and theorems can be named.

    axiom (idright) mul(A, e) = A
    axiom (idleft)  mul(e, A) = A
    axiom (assoc)   mul(A, mul(B, C)) = mul(mul(A, B), C)
    theorem (idcomm)
        mul(A, e) = mul(e, A)
    proof
        A = A
        mul(A, e) = A
        mul(A, e) = mul(e, A)
    qed
    ===> ok
