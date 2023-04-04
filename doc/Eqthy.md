Eqthy
=====

Description of the Language
---------------------------

An Eqthy document consists of any number of axioms and theorems.  Each
axiom is an equation.  An equation equates two terms.  Terms consist of
constructors (also called function symbols) and variables.  Variables begin
with uppercase letters.  Constructors begin with lowercase letters and are
followed by a list of zero or more subterms, enclosed in parentheses.  If a
term has no subterms, it is called an "atom" and the parentheses may be
omitted.

Each axiom may optionally by named.  Here are some example axioms:

    axiom (#id-right) mul(A, e) = A
    axiom (#id-left)  mul(e, A) = A
    axiom (#assoc)    mul(A, mul(B, C)) = mul(mul(A, B), C)

A theorem gives an equation, followed by a sequence of equations that shows
that the equation can be derived using the available means.  The available
means are:

*   the axioms that have been previously defined
*   the theorems that have been previously proved
*   the rules of inference of [equational logic](Equational-Logic.md)

The sequence of equations following a theorem is a proof.  Each equation in
the proof is optionally annotated with a hint that follows it, indicating what
axiom, theorem, or rule of inference was used to derive it.

    theorem (#id-comm)
        mul(A, e) = mul(e, A)
    proof
        A = A                   [by reflexivity]
        mul(A, e) = A           [by #id-right on LHS]
        mul(A, e) = mul(e, A)   [by #id-left on RHS]
    qed

Each step in a theorem can be checked for validity by a processor.  The processor
may be a computer program.  During this checking, the processor has access to all
the axioms and all the theories previously given in this Eqthy document
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

The rules of substitution and congruence may also be invoked; they may require a hint,
as it is sometimes not obvious what is being substituted where.

    e = e                                                [by reflexivity]
    mul(C, inv(C)) = e                                   [by #inverse on LHS]
    mul(mul(A, B), inv(mul(A, B))) = e                   [by substitution of mul(A, B) for C]
    mul(A, mul(mul(A, B), inv(mul(A, B)))) = mul(A, e)   [by congruence of B and mul(A, B)]

Once the processor has resolved what rules were applies and checked that the proof is
valid, it can _pretty-print_ an _annotated_ version of the input Eqthy document, one which
includes all of the hints that it inferred.  This pretty-printed document can be checked
again in the future, and more efficiently, as all the searches for hints have been
already performed.

Prescriptive Examples
---------------------

We now present a number of example Eqthy documents in
Falderal format, in the hopes that they will help clarify
the semantics of the language.

    -> Functionality "Parse Eqthy Document" is implemented by shell command
    -> "python3 bin/eqthy --bare --dump-ast %(test-body-file) 2>&1 > /dev/null && echo 'ok'"

### Parse Eqthy Document

    -> Tests for functionality "Parse Eqthy Document"

This document is well-formed.  It will parse.

    axiom inv(A) = A
    ===> ok

This document is not well-formed.  It will not parse.

    axiom inv(A) .
    ???> 

Comments are introduced with the symbol sequence `//`.  They extend
until the end of the line.

    // This is a comment.
    axiom inv(A) = A  // This is also a comment.
    ===> ok

### Check Eqthy Document

    -> Functionality "Check Eqthy Document" is implemented by shell command
    -> "python3 bin/eqthy --bare %(test-body-file) && echo 'ok'"

    -> Tests for functionality "Check Eqthy Document"

This document consists of some axioms and a theorem.

    axiom mul(A, e) = A
    axiom mul(e, A) = A
    axiom mul(A, mul(B, C)) = mul(mul(A, B), C)
    theorem
        mul(A, e) = A
    proof
        A = A
        mul(A, e) = A
    qed
    ===> ok

A document may contain more than one theorem.

    axiom mul(A, e) = A
    axiom mul(e, A) = A
    axiom mul(A, mul(B, C)) = mul(mul(A, B), C)
    theorem
        mul(A, e) = mul(e, A)
    proof
        A = A
        mul(A, e) = A
        mul(A, e) = mul(e, A)
    qed
    theorem
        mul(e, A) = mul(A, e)
    proof
        A = A
        A = mul(A, e)
        mul(e, A) = mul(A, e)
    qed
    ===> ok

Subsequent theorems can build on the results of previously-proved
theorems.

(TODO: this is definitely not the best example; give a better one.)

    axiom mul(A, e) = A
    axiom mul(e, A) = A
    axiom mul(A, mul(B, C)) = mul(mul(A, B), C)
    theorem
        mul(e, A) = mul(A, e)
    proof
        A = A
        A = mul(A, e)
        mul(e, A) = mul(A, e)
    qed
    theorem
        A = mul(A, e)
    proof
        A = A
        A = mul(e, A)
        A = mul(A, e)
    qed
    ===> ok

Any variable name you like can be used in a theorem.

    axiom mul(A, e) = A
    axiom mul(e, A) = A
    axiom mul(A, mul(B, C)) = mul(mul(A, B), C)
    theorem
        mul(Z, e) = Z
    proof
        Z = Z
        mul(Z, e) = Z
    qed
    ===> ok

This "proof" contains a misstep.

    axiom mul(A, e) = A
    axiom mul(e, A) = A
    axiom mul(A, mul(B, C)) = mul(mul(A, B), C)
    theorem
        mul(A, e) = mul(foo, mul(e, A))
    proof
        A = A
        mul(A, e) = A
        mul(A, e) = mul(foo, mul(e, A))
    qed
    ???> Could not derive mul(A, e) = mul(foo, mul(e, A)) from mul(A, e) = A

This theorem does not prove what it says it proves.

    axiom mul(A, e) = A
    axiom mul(e, A) = A
    axiom mul(A, mul(B, C)) = mul(mul(A, B), C)
    theorem
        mul(A, e) = mul(A, A)
    proof
        A = A
        mul(A, e) = A
    qed
    ???> No step in proof of unnamed_theorem_1 showed mul(A, e) = mul(A, A)

Typically, all theorems that are given in the document are checked,
and are checked in sequence, and checking stops at the first failure.

    axiom mul(A, e) = A
    axiom mul(e, A) = A
    axiom mul(A, mul(B, C)) = mul(mul(A, B), C)
    theorem
        mul(A, e) = mul(e, A)
    proof
        A = A
        mul(A, e) = A
        mul(A, e) = mul(e, A)
    qed
    theorem
        mul(e, A) = mul(A, e)
    proof
        A = A
        A = mul(A, e)
        mul(e, A) = mul(A, A)
    qed
    theorem
        mul(e, A) = mul(A, e)
    proof
        A = A
        A = mul(A, e)
        mul(e, A) = mul(e, A)
    qed
    ???> Could not derive mul(e, A) = mul(A, A) from A = mul(A, e)

This proof requires rewrites on the right-hand side of the equation.

    axiom mul(A, e) = A
    axiom mul(e, A) = A
    axiom mul(A, mul(B, C)) = mul(mul(A, B), C)
    theorem
        mul(A, e) = mul(e, A)
    proof
        A = A
        mul(A, e) = A
        mul(A, e) = mul(e, A)
    qed
    ===> ok

Axioms and theorems can be named.

    axiom (idright) mul(A, e) = A
    axiom (idleft)  mul(e, A) = A
    axiom (assoc)   mul(A, mul(B, C)) = mul(mul(A, B), C)
    theorem (idcomm)
        mul(A, e) = mul(e, A)
    proof
        A = A
        mul(A, e) = A
        mul(A, e) = mul(e, A)
    qed
    ===> ok

The name of an axiom or a theorem can either begin with an alphabetic
character, or it can begin with a `#` symbol.  If it begins with a `#`
symbol, it may contain `-` symbols.

    axiom (#id-right) mul(A, e) = A
    axiom (#id-left)  mul(e, A) = A
    axiom (#assoc)   mul(A, mul(B, C)) = mul(mul(A, B), C)
    theorem (#id-comm)
        mul(A, e) = mul(e, A)
    proof
        A = A
        mul(A, e) = A [by #id-right]
        mul(A, e) = mul(e, A)
    qed
    ===> ok

#### Hints

Proof steps can name the axiom being used in a hint written next to
the step.

    axiom (idright) mul(A, e) = A
    axiom (idleft)  mul(e, A) = A
    axiom (assoc)   mul(A, mul(B, C)) = mul(mul(A, B), C)
    theorem
        A = mul(A, e)
    proof
        A = A
        A = mul(A, e)  [by idright]
    qed
    ===> ok

Naming an axiom in a hint when the axiom used was not actually used there
is incorrect.  It is reasonable to (at least) warn the user of this mistake.

    axiom (idright) mul(A, e) = A
    axiom (idleft)  mul(e, A) = A
    axiom (assoc)   mul(A, mul(B, C)) = mul(mul(A, B), C)
    theorem
        A = mul(A, e)
    proof
        A = A
        A = mul(A, e)  [by idleft]
    qed
    ???> Could not derive A = mul(A, e) from A = A

Proof steps can also name a previously-proved theorem in a hint.

    axiom (idright) mul(A, e) = A
    axiom (idleft)  mul(e, A) = A
    axiom (assoc)   mul(A, mul(B, C)) = mul(mul(A, B), C)
    theorem (idcomm)
        mul(e, A) = mul(A, e)
    proof
        A = A
        A = mul(A, e)
        mul(e, A) = mul(A, e)
    qed
    theorem (something)
        A = mul(A, e)
    proof
        A = A
        A = mul(e, A)
        A = mul(A, e)   [by idcomm]
    qed
    ===> ok

Naming a theorem in a hint when the theorem used was not actually used there
is incorrect.  It is reasonable to (at least) warn the user of this mistake.

    axiom (idright) mul(A, e) = A
    axiom (idleft)  mul(e, A) = A
    axiom (assoc)   mul(A, mul(B, C)) = mul(mul(A, B), C)
    theorem (idcomm)
        mul(e, A) = mul(A, e)
    proof
        A = A
        A = mul(A, e)
        mul(e, A) = mul(A, e)
    qed
    theorem (something)
        A = mul(A, e)
    proof
        A = A
        A = mul(e, A)
        A = mul(A, A)   [by idcomm]
    qed
    ???> Could not derive A = mul(A, A) from A = mul(e, A)

When naming an axiom or theorem in a hint, variables used in that
axiom or theorem can be renamed before it is applied to the current step.

    axiom (idright) mul(A, e) = A
    axiom (idleft)  mul(e, A) = A
    axiom (assoc)   mul(A, mul(B, C)) = mul(mul(A, B), C)
    theorem
        R = mul(R, e)
    proof
        R = R
        R = mul(R, e)  [by idright with A=R]
    qed
    ===> ok

Using the reflexivity hint when the rule used was not actually reflexivity
is incorrect.  It is reasonable to (at least) warn the user of this mistake.

    axiom (idright) mul(A, e) = A
    axiom (idleft)  mul(e, A) = A
    axiom (assoc)   mul(A, mul(B, C)) = mul(mul(A, B), C)
    theorem
        A = mul(A, e)
    proof
        A = A
        A = mul(A, e) [by reflexivity]
    qed
    ???> Reflexivity

Proof steps can use the "substitution" hint.

    axiom (idright) mul(A, e) = A
    axiom (idleft)  mul(e, A) = A
    axiom (assoc)   mul(A, mul(B, C)) = mul(mul(A, B), C)
    theorem
        mul(mul(e, B), e) = mul(e, B)
    proof
        A = A
        mul(A, e) = A
        mul(mul(e, B), e) = mul(e, B)   [by substitution of mul(e, B) into A]
    qed
    ===> ok

In a substitution hint, the "into" part must name a variable.

    axiom (idright) mul(A, e) = A
    axiom (idleft)  mul(e, A) = A
    axiom (assoc)   mul(A, mul(B, C)) = mul(mul(A, B), C)
    theorem
        mul(mul(e, B), e) = mul(e, B)
    proof
        A = A
        mul(A, e) = A
        mul(mul(e, B), e) = mul(e, B)   [by substitution of mul(e, B) into mul(e, e)]
    qed
    ???> Expected variable

Using the substitution hint when the rule used was not actually substitution
is incorrect.  It is reasonable to (at least) warn the user of this mistake.

    axiom (idright) mul(A, e) = A
    axiom (idleft)  mul(e, A) = A
    axiom (assoc)   mul(A, mul(B, C)) = mul(mul(A, B), C)
    theorem
        mul(A, e) = A
    proof
        A = A
        mul(A, e) = A             [by substitution of mul(A, e) into A]
    qed
    ???> Substitution

Proof steps can use the "congruence" hint.

    axiom (idright) mul(A, e) = A
    axiom (idleft)  mul(e, A) = A
    axiom (assoc)   mul(A, mul(B, C)) = mul(mul(A, B), C)
    theorem
        mul(B, mul(A, e)) = mul(B, A)
    proof
        A = A
        mul(A, e) = A
        mul(B, mul(A, e)) = mul(B, A)     [by congruence of A and mul(B, A)]
    qed
    ===> ok

In a congruence hint, the first part must name a variable.

    axiom (idright) mul(A, e) = A
    axiom (idleft)  mul(e, A) = A
    axiom (assoc)   mul(A, mul(B, C)) = mul(mul(A, B), C)
    theorem
        mul(B, mul(A, e)) = mul(B, A)
    proof
        A = A
        mul(A, e) = A
        mul(B, mul(A, e)) = mul(B, A)     [by congruence of mul(B, A) and A]
    qed
    ???> Expected variable

Using the congruence hint when the rule used was not actually substitution
is incorrect.  It is reasonable to (at least) warn the user of this mistake.

    axiom (idright) mul(A, e) = A
    axiom (idleft)  mul(e, A) = A
    axiom (assoc)   mul(A, mul(B, C)) = mul(mul(A, B), C)
    theorem
        mul(A, e) = A
    proof
        A = A
        mul(A, e) = A             [by congruence of A and mul(A, e)]
    qed
    ???> Congruence
