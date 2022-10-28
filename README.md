Eqthy
=====

**Eqthy** is a language for equational proofs, designed to be both
machine-readable and human-usable.  It strongly resembles equational
styles of proof as they are often found in introductory textbooks,
where each line follows from the previous line.

Here is an example of what an Eqthy proof looks like:

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
tests, see [doc/Eqthy.md](doc/Eqthy.md).

The language does not prescribe any specific usage but it is expected
that one of the main reasons for a computer to read a proof written
in Eqthy would be to check it for validity.

This distribution contains such a proof checker, written in Python 3.
The source code for it can be found in the [src/](src/) directory.

TODO
----

*   `[by previous_theorem]`
*   Document the Syntax for Comments
*   impl: show step number or line number when cannot derive next step
