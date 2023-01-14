Group Element Commutes with Inverse
===================================

See [Group Element Commutes with Inverse](https://proofwiki.org/wiki/Group_Element_Commutes_with_Inverse)
on proofwiki.org.

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
