Eqthy
=====

_Version 0.0_ | _See also:_ [Philomath](https://github.com/catseye/Philomath#readme)
∘ [LCF-style-ND](https://github.com/cpressey/LCF-style-ND#readme)

- - - -

**Eqthy** is a language for equational proofs.  It is designed to be both
machine-readable and human-usable.  It strongly resembles the equational
style sometimes used in introductory textbooks, where each line follows
from the previous line, and may optionally give a justification for the
proof step.  Here is an example:

    axiom (id-right) mul(A, e) = A
    axiom (id-left)  mul(e, A) = A
    axiom (assoc)    mul(A, mul(B, C)) = mul(mul(A, B), C)
    theorem (id-comm)
        mul(A, e) = mul(e, A)
    proof
        A = A
        mul(A, e) = A           [by id-right]
        mul(A, e) = mul(e, A)   [by id-left]
    qed

For a fuller description of the language, including a set of Falderal
tests, see **[doc/Eqthy.md](doc/Eqthy.md)**.

A number of proofs have been written in Eqthy.  These can be found in
the **[eg/](eg/)** directory.

### Implementations

The language does not prescribe any specific usage but it is expected
that one of the main reasons for a computer to read a proof written
in Eqthy would be to check it for validity.

This distribution contains such a proof checker, written in Python 3.
The source code for it can be found in the **[src/](src/)** directory.

The core module that does proof checking,
**[eqthy.verifier](src/eqthy/verifier.py)**, is less than 200 lines in length,
despite having many logging statements.  The hope is to make investigating
and understanding its behaviour as un-intimidating as possible.

TODO
----

*   Handle "on LHS", "on RHS" in hints.
*   Demonstrate multiple theorems, and that previous theorems can be used
    as justifications in proof steps.
*   Show the step number or line number in the error message when
    there is a derivation error.
*   Allow rules to be instantiated with variable names other than the
    ones that are specified in the rule.
