Eqthy
=====

This document provides a number of example Eqthy document in
Falderal format, in the hopes that they will help clarify
the semantics of the language.
For an overview of the language, see the README file.

    -> Functionality "Parse Eqthy Document" is implemented by shell command
    -> "python3 bin/eqthy --dump-ast %(test-body-file)"

### Parse Eqthy Document

    -> Tests for functionality "Parse Eqthy Document"

This document is well-formed.  It will parse.

    axiom inv(A) = A
    ===> Development(axioms=[Axiom(name=None, eqn=Eqn(lhs=Term(ctor='inv', subterms=[Variable(name='A')]), rhs=Variable(name='A')))], theorems=[])

This document is not well-formed.  It will not parse.

    axiom inv(A) .
    ???> Expected '=', but found '.'

### Check Eqthy Document

    -> Functionality "Check Eqthy Document" is implemented by shell command
    -> "python3 bin/eqthy %(test-body-file) && echo 'ok'"

    -> Tests for functionality "Check Eqthy Document"

This document consists of some axioms and a theorem.

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

#### Hints

Proof steps can name the axiom being used in a hint written next to
the step.

    axiom (idright) mul(A, e) = A
    axiom (idleft)  mul(e, A) = A
    axiom (assoc)   mul(A, mul(B, C)) = mul(mul(A, B), C)
    theorem
        A = mul(A, e)
    proof
        A = A
        A = mul(A, e)  [by idright]
    qed
    ===> ok

Naming an axiom in a hint when the axiom used was not actually used there
is incorrect.  It is reasonable to (at least) warn the user of this mistake.

    axiom (idright) mul(A, e) = A
    axiom (idleft)  mul(e, A) = A
    axiom (assoc)   mul(A, mul(B, C)) = mul(mul(A, B), C)
    theorem
        A = mul(A, e)
    proof
        A = A
        A = mul(A, e)  [by idleft]
    qed
    ???> waaaaa

Using the reflexivity hint when the rule used was not actually reflexivity
is incorrect.  It is reasonable to (at least) warn the user of this mistake.

    axiom (idright) mul(A, e) = A
    axiom (idleft)  mul(e, A) = A
    axiom (assoc)   mul(A, mul(B, C)) = mul(mul(A, B), C)
    theorem
        A = mul(A, e)
    proof
        A = A
        A = mul(A, e) [by reflexivity]
    qed
    ???> Incorrect hint

Proof steps can use the "substitution" hint.

    axiom (idright) mul(A, e) = A
    axiom (idleft)  mul(e, A) = A
    axiom (assoc)   mul(A, mul(B, C)) = mul(mul(A, B), C)
    theorem
        mul(mul(e, B), e) = mul(e, B)
    proof
        A = A
        mul(A, e) = A
        mul(mul(e, B), e) = mul(e, B)   [by substitution of mul(e, B) into A]
    qed
    ===> ok

In a substitution hint, the "into" part must name a variable.

    axiom (idright) mul(A, e) = A
    axiom (idleft)  mul(e, A) = A
    axiom (assoc)   mul(A, mul(B, C)) = mul(mul(A, B), C)
    theorem
        mul(mul(e, B), e) = mul(e, B)
    proof
        A = A
        mul(A, e) = A
        mul(mul(e, B), e) = mul(e, B)   [by substitution of mul(e, B) into mul(e, e)]
    qed
    ???> Expected variable

Using the substitution hint when the rule used was not actually substitution
is incorrect.  It is reasonable to (at least) warn the user of this mistake.

    axiom (idright) mul(A, e) = A
    axiom (idleft)  mul(e, A) = A
    axiom (assoc)   mul(A, mul(B, C)) = mul(mul(A, B), C)
    theorem
        mul(A, e) = A
    proof
        A = A
        mul(A, e) = A             [by substitution of mul(A, e) into A]
    qed
    ???> ok

Proof steps can use the "congruence" hint.

    axiom (idright) mul(A, e) = A
    axiom (idleft)  mul(e, A) = A
    axiom (assoc)   mul(A, mul(B, C)) = mul(mul(A, B), C)
    theorem
        mul(B, mul(A, e)) = mul(B, A)
    proof
        A = A
        mul(A, e) = A
        mul(B, mul(A, e)) = mul(B, A)     [by congruence of A and mul(B, A)]
    qed
    ===> ok

In a congruence hint, the first part must name a variable.

    axiom (idright) mul(A, e) = A
    axiom (idleft)  mul(e, A) = A
    axiom (assoc)   mul(A, mul(B, C)) = mul(mul(A, B), C)
    theorem
        mul(B, mul(A, e)) = mul(B, A)
    proof
        A = A
        mul(A, e) = A
        mul(B, mul(A, e)) = mul(B, A)     [by congruence of mul(B, A) and A]
    qed
    ???> Expected variable

Using the congruence hint when the rule used was not actually substitution
is incorrect.  It is reasonable to (at least) warn the user of this mistake.

    axiom (idright) mul(A, e) = A
    axiom (idleft)  mul(e, A) = A
    axiom (assoc)   mul(A, mul(B, C)) = mul(mul(A, B), C)
    theorem
        mul(A, e) = A
    proof
        A = A
        mul(A, e) = A             [by congruence of A and mul(A, e)]
    ???> ok
