Eqthy
=====

**Eqthy** is a language for equational proofs.  It's similar to, but different from, the "calculational style"
developed and popularized by Dijkstra et al.

This document is a sketch.  It describes the language.  It mentions some things a processor of the language
might be expected to do.

An Eqthy source consists of any number of axioms and theorems.  Each axiom is an equation.
An equation equates two terms.  Terms consist of constructors (also called function symbols)
and variables.  Variables begin with uppercase letters.  Constructors begin with lowercase
letters are followed by a list of zero or more subterms, enclosed in parentheses.
If a term has no subterms, it is called an "atom" and the parentheses may be omitted.

Each axiom may optionally by named.  Here are some example axioms:

    axiom (#id-right) mul(A, e) = A
    axiom (#id-left)  mul(e, A) = A
    axiom (#assoc)    mul(A, mul(B, C)) = mul(mul(A, B), C)

A theorem gives an equation, followed by a sequence of equations that shows that the
validitiy of the equation follows from the axioms and theorems previously given in
the Eqthy souce.  Each equation in the sequence is optionally followed by a hint,
indicating what rule was used to derive it.

    theorem (#id-comm)
        mul(A, e) = mul(e, A)
    proof
        A = A                   [by reflexivity]
        mul(A, e) = A           [by #id-right on LHS]
        mul(A, e) = mul(e, A)   [by #id-left on RHS]
    qed

Each step in a theorem can be checked for validity by a processor.  The processor
may be a computer program.  During this checking, the processor has access to all
the axioms and all the theories previously given in this Eqthy source
(and possibly from shared libraries).  The checking process ensures that the first
step can be obtained from an axiom or previously proved theory, that each step
can be derived from the previous step, and that the equation being proved matches
the last step.  Once a theorem has been checked, the equation that was provded
is available for use in subsequent theorems.

The hint on each step is optional.  If omitted, it is assumed that the processor will do
what it can to search for what rule might have been applied, to derive this step from the previous
step.  It is also assumed that the processor may have limitations in this regard, so in
practice, the hint might not be optional on steps for which necessarily involve more searching.

Eqthy itself makes no assumption about the power of any particular processor to
search for derivations in the absence of hints.  A processor may not be able to
derive anything without hints, or it may not require any hints at all.  What is
required of a processor is that it does not allow a chain of steps which is invalid
to be reported as valid and subsequently used in other proofs.

In the above theorem, if we omit the hints, the processor must deduce by itself that:

*   `A = A` is an instance of reflexivity.  This is easy to see, because the LHS and RHS are
    identical.
*   `mul(A, e) = A` is an application of `#id-right` on the LHS.  This can be seen
    by searching through the available axioms and previously-proved theorem steps,
    to see which rewrite of `A = A` would result in `mul(A, e) = A`.
*   The third step is similar to the second.

Additionally, if the step `B = A` appears immediately after `A = B`, it can infer that
the rule of symmetry was invoked.

Once the processor has resolved what rules were applies and checked that the proof is
valid, it can _pretty-print_ an _annotated_ version of the input Eqthy source, one which
includes all of the hints that it inferred.  This pretty-printed source can be checked
again in the future, and more efficiently, as all the searches for hints have been
already performed.
