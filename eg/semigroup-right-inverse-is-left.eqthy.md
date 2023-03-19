Right Inverse for All is Left Inverse
=====================================

See [Right Inverse for All is Left Inverse](https://proofwiki.org/wiki/Right_Inverse_for_All_is_Left_Inverse)
on proofwiki.org.

First we need the semigroup axioms.

    axiom (#id-right)  mul(A, e) = A
    axiom (#assoc)     mul(A, mul(B, C)) = mul(mul(A, B), C)
    axiom (#inv-right) mul(A, inv(A)) = e

Next we need "Product of Semigroup Element with Right Inverse is Idempotent"
as a lemma.

    theorem (#product-of-semigroup-element-with-right-inverse-is-idempotent)
        mul(mul(inv(A), A), mul(inv(A), A)) = mul(inv(A), A)
    proof
        mul(inv(A), A) = mul(inv(A), A)
        mul(mul(inv(A), e), A) = mul(inv(A), A)
        mul(mul(inv(A), mul(A, inv(A))), A) = mul(inv(A), A)
        mul(mul(mul(inv(A), A), inv(A)), A) = mul(inv(A), A)
        mul(mul(inv(A), A), mul(inv(A), A)) = mul(inv(A), A)
    qed

Finally we need this proof.

    theorem (#right-inverse-for-semigroup-is-left-inverse)
        mul(inv(A), A) = e
    proof
        e = e
        mul(A, inv(A)) = e
        mul(mul(inv(A), A), inv(mul(inv(A), A))) = e
                                                        [by substitution of mul(inv(A), A) into A]
        mul(mul(mul(inv(A), A), mul(inv(A), A)), inv(mul(inv(A), A))) = e
                                                        [by #product-of-semigroup-element-with-right-inverse-is-idempotent]
        mul(mul(inv(A), A), mul(mul(inv(A), A), inv(mul(inv(A), A)))) = e
        mul(mul(inv(A), A), e) = e
        mul(inv(A), A) = e
    qed
