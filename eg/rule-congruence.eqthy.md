Rule: Congruence
================

Demonstration of the use of Congruence in a proof.
(This is not something the `eqthy` checker searches for,
so it does have to be given explicitly in the justification.)

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
