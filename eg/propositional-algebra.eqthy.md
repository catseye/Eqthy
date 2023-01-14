Propositional Algebra
=====================

_NOTE: still under development_

This is a possible formulation of propositional algebra in Eqthy.  For some background,
see Section II of [An Algebraic Introduction to Mathematical Logic][] (Barnes and Mack, 1975)
but note that, while this follows the general ideas there, it might not follow them closely.

`th(X, ...)` indicates that X is in the list of theorems.  There may be more theorems
in the ..., i.e. it is like a cons list.  `e` indicates the empty set of theorems. 
The order that the theorems appear in the list does not matter.

    axiom th(X, th(Y, Z)) = th(th(X, Y), Z)
    axiom th(X, Y) = th(Y, X)

The logic system is a Hilbert-style system.  There are three statements that are axioms.
We model this by saying that any set of theorems T is equal to T with any of these
extra axiomatic statements added to it.

    axiom th(X, e) = th(X, th(impl(impl(P, Q), P), e))
    axiom th(X, e) = th(X, th(impl(impl(P, impl(Q, R)), impl(impl(P, Q), impl(P, R)), e)))
    axiom th(X, e) = th(X, th(impl(not(not(P)), P), e))

In addition, we have modus ponens.

    axiom th(P, th(impl(P, Q), e)) = th(Q, th(P, th(impl(P, Q), e)))

I believe this should work.  So, let's pick a simple proof and write it up and see if
the `eqthy` checker can confirm it.  Example 4.5 on page 16 of Barnes and Mack:

>   |- p => p

We write this in equational logic by saying that any set of theorems is equal to a
set of theorems which contains this theorem.

    // theorem
    //    th(X, e) = th(X, th(impl(P, P), e))

The proof given in the book is

> p1 = p => ((p => p) => p)  
> p2 = (p => ((p => p) => p)) => ((p => (p => p)) => (p=>p))  
> p3 = (p => (p => p)) => (p => p)  
> p4 = p => (p => p)  
> p5 = p => p  

And now we... mechanically translate that...

    // proof
    //     TODO = TODO
    // qed

[An Algebraic Introduction to Mathematical Logic]: https://archive.org/details/algebraicintrodu00barn_0
