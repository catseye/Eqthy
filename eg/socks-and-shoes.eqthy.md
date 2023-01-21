Socks and Shoes
===============

See [Socks and shoes proof](https://en.wikiversity.org/wiki/Introduction_to_group_theory/Socks_and_shoes_proof)
on Wikiversity.

Also see [Inverse of Product](https://proofwiki.org/wiki/Inverse_of_Product) on ProofWiki.

    axiom (#id-right) mul(A, e) = A
    axiom (#id-left)  mul(e, A) = A
    axiom (#assoc)    mul(A, mul(B, C)) = mul(mul(A, B), C)
    axiom (#invA1)    mul(A, inv(A)) = e
    axiom (#invA2)    mul(inv(A), A) = e  // FIXME: should be shown as a theorem
    axiom (#invB1)    mul(B, inv(B)) = e  // FIXME: should be possible to rename variables by choice when applying an axiom
    axiom (#invB2)    mul(inv(B), B) = e

    theorem (#socks-and-shoes)
        inv(mul(A, B)) = mul(inv(B), inv(A))
    proof
        e = e
        mul(A, inv(A)) = e

        mul(mul(A, B), inv(mul(A, B))) = e                 [by substitution of mul(A, B) into A]
        mul(mul(A, B), inv(mul(A, B))) = mul(A, inv(A))
        mul(mul(A, B), inv(mul(A, B))) = mul(mul(A, e), inv(A))
        mul(mul(A, B), inv(mul(A, B))) = mul(mul(A, mul(B, inv(B))), inv(A))
        mul(mul(A, B), inv(mul(A, B))) = mul(mul(mul(A, B), inv(B)), inv(A))
        mul(mul(A, B), inv(mul(A, B))) = mul(mul(A, B), mul(inv(B), inv(A)))

        mul(inv(A), mul(mul(A, B), inv(mul(A, B)))) = mul(inv(A), mul(mul(A, B), mul(inv(B), inv(A))))  [by congruence of C and mul(inv(A), C)]
        mul(mul(inv(A), mul(A, B)), inv(mul(A, B))) = mul(inv(A), mul(mul(A, B), mul(inv(B), inv(A))))
        mul(mul(mul(inv(A), A), B), inv(mul(A, B))) = mul(inv(A), mul(mul(A, B), mul(inv(B), inv(A))))
        mul(mul(e, B), inv(mul(A, B))) = mul(inv(A), mul(mul(A, B), mul(inv(B), inv(A))))
        mul(B, inv(mul(A, B))) = mul(inv(A), mul(mul(A, B), mul(inv(B), inv(A))))

        mul(B, inv(mul(A, B))) = mul(mul(inv(A), mul(A, B)), mul(inv(B), inv(A)))
        mul(B, inv(mul(A, B))) = mul(mul(mul(inv(A), A), B), mul(inv(B), inv(A)))
        mul(B, inv(mul(A, B))) = mul(mul(e, B), mul(inv(B), inv(A)))
        mul(B, inv(mul(A, B))) = mul(B, mul(inv(B), inv(A)))

        mul(inv(B), mul(B, inv(mul(A, B)))) = mul(inv(B), mul(B, mul(inv(B), inv(A))))  [by congruence of C and mul(inv(B), C)]
        mul(mul(inv(B), B), inv(mul(A, B))) = mul(inv(B), mul(B, mul(inv(B), inv(A))))
        mul(mul(inv(B), B), inv(mul(A, B))) = mul(mul(inv(B), B), mul(inv(B), inv(A)))
        mul(e, inv(mul(A, B))) = mul(mul(inv(B), B), mul(inv(B), inv(A)))
        mul(e, inv(mul(A, B))) = mul(e, mul(inv(B), inv(A)))
        inv(mul(A, B)) = mul(e, mul(inv(B), inv(A)))
        inv(mul(A, B)) = mul(inv(B), inv(A))

    qed