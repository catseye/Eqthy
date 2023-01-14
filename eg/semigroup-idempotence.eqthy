Product of Semigroup Element with Right Inverse is Idempotent
=============================================================

See [Product of Semigroup Element with Right Inverse is Idempotent](https://proofwiki.org/wiki/Product_of_Semigroup_Element_with_Right_Inverse_is_Idempotent)
on proofwiki.org.

    axiom (#id-right)  mul(A, e) = A
    axiom (#assoc)     mul(A, mul(B, C)) = mul(mul(A, B), C)
    axiom (#inv-right) mul(A, inv(A)) = e

    theorem (#product-of-semigroup-element-with-right-inverse-is-idempotent)
        mul(mul(inv(A), A), mul(inv(A), A)) = mul(inv(A), A)
    proof
        mul(inv(A), A) = mul(inv(A), A)
        mul(mul(inv(A), e), A) = mul(inv(A), A)
        mul(mul(inv(A), mul(A, inv(A))), A) = mul(inv(A), A)
        mul(mul(mul(inv(A), A), inv(A)), A) = mul(inv(A), A)
        mul(mul(inv(A), A), mul(inv(A), A)) = mul(inv(A), A)
    qed
