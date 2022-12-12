Eqthy
=====

_Version 0.0_ | _See also:_ [Philomath](https://github.com/catseye/Philomath#readme)
∘ [LCF-style-ND](https://github.com/cpressey/LCF-style-ND#readme)

- - - -

**Eqthy** is a formalized language for equational proofs.  Its design attempts to
reconcile _simplicity of implementation on a machine_ with _human usability_
([more on this below](#design-principles)).  It supports an elementary linear
style, where each line gives a step which is derived from the step on the previous
line, and may optionally state the justification for the derivation in that step.
Here is an example:

    axiom (idright) mul(A, e) = A
    axiom (idleft)  mul(e, A) = A
    axiom (assoc)   mul(A, mul(B, C)) = mul(mul(A, B), C)
    theorem (idcomm)
        mul(A, e) = mul(e, A)
    proof
        A = A
        mul(A, e) = A           [by idright]
        mul(A, e) = mul(e, A)   [by idleft]
    qed

For a fuller description of the language, including a set of Falderal
tests, see **[doc/Eqthy.md](doc/Eqthy.md)**.

A number of proofs have been written in Eqthy to date.  These can be found in
the **[eg/](eg/)** directory.  In particular, there is a worked-out
proof of the [Socks and Shoes](eg/socks-and-shoes.eqthy) theorem in
group theory, with hopefully more coming soon.

The Eqthy language is still at an early stage and is subject to change.  Since
the idea is to accumulate a database of proofs which can be built upon, it is
unlikely that the format of the language will change radically.

### Design Principles

Probably the language that Eqthy most resembles, in spirit, is
[Metamath][]; but its underlying mechanics are rather different.
Eqthy is based on [equational logic][], so each step is an equation.

Eqthy's design attempts to reconcile simplicity of implementation on a machine
with human usability.  It should be understood that this is a balancing act;
adding features to the language which improve usability will generally be
detrimental to simplicity, and vice versa.

It has been implemented in Python in about 550 lines of code; the core
verifier module is less than 200 lines of code.  For more details, see
the [Implementations](#implementations) section below.

It is also possible for a human to write Eqthy documents by hand, and
to read them, without much specialized knowledge.  The base logic
is [equational logic][], which has only 5 rules of inference, and these
rules are particularly widely understood; "replace equals with equals" is
a standard part of the high-school algebra cirriculum.

(In comparison, `mmverifier.py`, a Python implementation of a Metamath
checker, is 360 lines of code; and while it is undoubtedly simple, the
Metamath language is not widely regarded as being easy to write or read.)

### Implementations

While the language does not prescribe any specific usage for proofs
written in Eqthy, it is reasonable to expect that one of the main reasons
for a computer to read one would be to check it for validity.

This distribution contains such a proof checker, written in Python 3.
The source code for it can be found in the **[src/](src/)** directory.

The core module that does proof checking,
**[eqthy.verifier](src/eqthy/verifier.py)**, is less than 200 lines in length,
despite having many logging statements (which both act as comments, and provide a
trace to help the user understand the execution of the verifier on any given
document).

The desire is to make reading the code and understanding its behaviour as
un-intimidating as possible.

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

[Metamath]: https://us.metamath.org/
[equational logic]: doc/Equational-Logic.md
