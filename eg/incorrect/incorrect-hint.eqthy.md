    axiom (idright) mul(A, e) = A
    axiom (idleft)  mul(e, A) = A
    axiom (assoc)   mul(A, mul(B, C)) = mul(mul(A, B), C)
    theorem
        A = mul(A, e)
    proof
        A = A
        A = mul(A, e)  [by idleft]
    qed
