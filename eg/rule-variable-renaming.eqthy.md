Variable Renaming during Substitution
=====================================

This is [Product of Semigroup Element with Right Inverse is Idempotent](semigroup-idempotence.eqthy.md)
except with different variable names declared in the rules, showing that these names can be
renamed during substitution.

    axiom (#id-right)  mul(A, e) = A
    axiom (#assoc)     mul(A, mul(B, C)) = mul(mul(A, B), C)
    axiom (#inv-right) mul(R, inv(R)) = e

    theorem (#product-of-semigroup-element-with-right-inverse-is-idempotent)
        mul(mul(inv(A), A), mul(inv(A), A)) = mul(inv(A), A)
    proof
        mul(inv(A), A) = mul(inv(A), A)
        mul(mul(inv(A), e), A) = mul(inv(A), A)
        mul(mul(inv(A), mul(A, inv(A))), A) = mul(inv(A), A)  [by #inv-right with R=A]
        mul(mul(mul(inv(A), A), inv(A)), A) = mul(inv(A), A)
        mul(mul(inv(A), A), mul(inv(A), A)) = mul(inv(A), A)
    qed
