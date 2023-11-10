Eqthy
=====

_Version 0.3_ | _See also:_ [Philomath](https://codeberg.org/catseye/Philomath#philomath)
∘ [LCF-style-ND](https://codeberg.org/catseye/The-Dossier/src/branch/master/article/LCF-style-Natural-Deduction/README.md)

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

For improved human usability, Eqthy is usually embedded within Markdown documents.
This allows proofs to be written in a more "literate" style, with interspersed
explanatory prose and references in the form of hyperlinks.

For a fuller description of the language, including a set of Falderal
tests, see **[doc/Eqthy.md](doc/Eqthy.md)**.

A number of proofs have been written in Eqthy to date.  These can be found in
the **[eg/](eg/)** directory.  In particular, there are worked-out proofs:

*   of the [Socks and Shoes](eg/socks-and-shoes.eqthy.md) theorem in group theory;
*   in [Propositional Algebra](eg/propositional-algebra.eqthy.md);
*   in [Boolean Algebra](eg/boolean-algebra.eqthy.md), giving lemmas that could
    be used in a proof of De Morgan's laws;
*   in [Combinatory Logic](eg/combinatory-logic.eqthy.md),

with hopefully more to come in the future.

The Eqthy language is still at an early stage and is subject to change.  However,
since the idea is to accumulate a database of proofs which can be built upon,
it is unlikely that the format of the language will change radically.

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

While the language does not prescribe any specific application for proofs
written in Eqthy, it is reasonable to expect that one of the main reasons
one would want a computer to read one would be for it to check it for validity.

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

### Small Items

*   Handle "on LHS", "on RHS" in hints.
*   Allow context accumulated when verifying one document to be
    carried over and used when verifying the next documnet.
*   Allow the first line of a proof to be an axiom.
*   Scanner should report correct line number in errors
    when Eqthy document is embedded in Markdown.
*   Arity checking?  Would prevent some silly errors in axioms.

### Desired Examples

*   [Interior algebra](https://en.wikipedia.org/wiki/Interior_algebra) (corresponding to the modal logic S4)
*   [Relation algebra](https://en.wikipedia.org/wiki/Relation_algebra)
*   Johnson's 1892 axiom system given in Meredith and Prior's 1967 paper [Equational Logic](https://projecteuclid.org/download/pdf_1/euclid.ndjfl/1093893457)
*   The theorem of ring theory given in [Equational Logic, Spring 2017](https://people.math.sc.edu/mcnulty/alglatvar/equationallogic.pdf) by McNulty (but it's a bit of a monster all right)

### Aspirational Items

#### Preprocessor

It would make some sense to split off the code that
parses an Eqthy document into its own program, which the main
program calls when reading in an Eqthy document, much in the same
vein as the C preprocessor does.  This would necessitate defining
a simple intermediate format (S-expressions or JSON) by which the
preprocessor communicates the parsed document to the main prover.

This would allow the syntax to become more sophisticated (for
example, supporting infix syntax for operators) while the core
proof checker is unchanged.  And would allow re-implementing the
core proof checker in another language without necessitating
rewriting the entire parser too.

#### AC-unification

Or rather, AC-matching.  An awful lot of a typical Eqthy proof
involves merely rearranging things around operators that are
associative and/or commutative.  If Eqthy can be taught that

    add(add(1, 2), X)

matches

    add(2, add(3, 1))

with the unifier `X=3` because it has been informed that `add`
is an associative and commutative operator, then many proof steps
can be omitted.  The trick would be to have a simple syntax that
indicates this, and a simple implementation of matching that supports
it without adding too many lines of code to the proof checker.

#### Embedding in a Functional Programming Language

This may by its nature be a seperate project, as it would
involve creating a functional programming language of which Eqthy
is a subset.

The idea is that we would introduce a special form of axiom with
some additional connotations.  For example,

    def add(X, 0) => X

would be in all respects the same as

    axiom add(X, 0) = X

but with the additional connotation that when a term such as
`add(5, 0)` is "evaluated" it should "reduce" to `5`.  There
is no connotation from this that "evaluating" 5 should "reduce"
to anything however, but it would still be possible to appeal
to the equality `add(5, 0) = 5` in both directions in a proof
written in this language.

The practical upshot being that you could write small functional
programs and _also_ proofs of some of their properties, in this
one language, which is only a modest superset of Eqthy.

[Metamath]: https://us.metamath.org/
[equational logic]: doc/Equational-Logic.md
