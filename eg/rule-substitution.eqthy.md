Rule: Substitution
==================

Demonstration of the use of the Substitution rule in a proof.
(This is not something the `eqthy` checker searches for,
so it does have to be given explicitly in the justification.)

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
