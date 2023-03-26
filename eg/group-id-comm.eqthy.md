Group Element Commutes with Inverse
===================================

See [Group Element Commutes with Inverse](https://proofwiki.org/wiki/Group_Element_Commutes_with_Inverse)
on proofwiki.org.  (Although, this does not need even all the structure of a group; the axioms below
define a monoid.)

Note that this proof provides justifications on each step.  For a proof as simple as this one,
this isn't actually necessary, and if they were omitted, the `eqthy` checker would still be
able to verify that this proof is valid.  Indeed, the names of the axioms could be omitted as well.

    axiom (#id-right) mul(A, e) = A
    axiom (#id-left)  mul(e, A) = A
    axiom (#assoc)    mul(A, mul(B, C)) = mul(mul(A, B), C)

    theorem (#group-element-commutes-with-inverse)
        mul(A, e) = mul(e, A)
    proof
        A = A                   [by reflexivity]
        mul(A, e) = A           [by #id-right on LHS]
        mul(A, e) = mul(e, A)   [by #id-left on RHS]
    qed
