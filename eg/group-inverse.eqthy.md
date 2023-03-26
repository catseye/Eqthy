Group Inverse
=============

When working in abstract algebra, one sometimes proves that the identity
element is unique, or writes a proof leveraging that fact.  However, such
proofs cannot be written in a purely equational setting, where the
identity element has been defined, not with an existence axiom, but as
a nullary operator.

So other techniques need to be used when working in 
equational logic.

    axiom (#id-right)   mul(A, e) = A
    axiom (#id-left)    mul(e, A) = A
    axiom (#assoc)      mul(A, mul(B, C)) = mul(mul(A, B), C)
    axiom (#inv-right)  mul(A, inv(A)) = e
    axiom (#inv-left)   mul(inv(A), A) = e

### Inverse of Identity is Identity

    theorem
        inv(e) = e
    proof
        e = e
        mul(inv(e), e) = e     [by #inv-left with A=e]
        inv(e) = e
    qed

### Inverse of Group Inverse

Also see [Inverse of Group Inverse](https://proofwiki.org/wiki/Inverse_of_Group_Inverse) on ProofWiki.

    theorem
        inv(inv(A)) = A
    proof
        e = e
        e = mul(inv(A), A)
        mul(inv(inv(A)), e) = mul(inv(inv(A)), mul(inv(A), A))   [by congruence of X and mul(inv(inv(A)), X)]
        inv(inv(A)) = mul(inv(inv(A)), mul(inv(A), A))
        inv(inv(A)) = mul(mul(inv(inv(A)), inv(A)), A)
        inv(inv(A)) = mul(e, A)                                  [by #inv-left]
        inv(inv(A)) = A
    qed
