Eqthy
=====

_Version 0.0_ | _See also:_ [Philomath](https://github.com/catseye/Philomath#readme)
∘ [LCF-style-ND](https://github.com/cpressey/LCF-style-ND#readme)

- - - -

**Eqthy** is a simple formal language for equational proofs.  It is designed to be both
machine-readable and (just barely) human-usable.  It strongly resembles the equational
style sometimes used in textbooks, where each line is derived from the previous line,
and may optionally state the justification for the derivation in that step.
Here is an example:

    axiom (idright) mul(A, e) = A
    axiom (idleft)  mul(e, A) = A
    axiom (assoc)    mul(A, mul(B, C)) = mul(mul(A, B), C)
    theorem (idcomm)
        mul(A, e) = mul(e, A)
    proof
        A = A
        mul(A, e) = A           [by idright]
        mul(A, e) = mul(e, A)   [by idleft]
    qed

For a fuller description of the language, including a set of Falderal
tests, see **[doc/Eqthy.md](doc/Eqthy.md)**.

A number of proofs have been written in Eqthy.  These can be found in
the **[eg/](eg/)** directory.  In particular, there is a worked-out
proof of the [Socks and Shoes](eg/socks-and-shoes.eqthy) theorem in
group theory, with hopefully more coming soon.

### Implementations

While the language does not prescribe any specific usage for proofs
written in Eqthy, it is reasonable to expect that one of the main reasons
for a computer to read one would be to check it for validity.

This distribution contains such a proof checker, written in Python 3.
The source code for it can be found in the **[src/](src/)** directory.

The core module that does proof checking,
**[eqthy.verifier](src/eqthy/verifier.py)**, is less than 200 lines in length,
despite having many logging statements.  The desire is to make reading it
and understanding its behaviour as un-intimidating as possible.

TODO
----

*   Handle "on LHS", "on RHS" in hints.
*   Show the step number or line number in the error message when
    there is a derivation error.
*   Allow rules to be instantiated with variable names other than the
    ones that are specified in the rule.
*   Decide what happens when multiple files are given on the command line.
    Simply concatenating them does not play well with a grammar where
    axioms cannot follow theorems.  Ideally we would want to trace the
    source file name for error reporting too.
