Propositional Algebra
=====================

This is one possible formulation of propositional algebra in Eqthy.  For some background,
see Section II of [An Algebraic Introduction to Mathematical Logic][] (Barnes and Mack, 1975)
but note that, while this follows the general ideas there, it might not follow them very closely.

`th(X, ...)` indicates that X is in the list of theorems.  There may be more theorems
in the ..., i.e. it is like a cons list.  `e` indicates the empty set of theorems. 
The order that the theorems appear in the list does not matter.

    axiom (#th-assoc) th(X, th(Y, Z)) = th(th(X, Y), Z)
    axiom (#th-comm)  th(X, th(Y, Z)) = th(Y, th(X, Z))

The logic system is a Hilbert-style system, with three axioms.
In Barnes and Mack, the axioms are given "semantically", using set comprehensions
(p. 15):

> A1 = {_p_ ⇒ (_q_ ⇒ _p_) | _p_, _q_ ∈ _P_(_X_)}  
> A2 = {(_p_ ⇒ (_q_ ⇒ _r_)) ⇒ ((_p_ ⇒ _q_) ⇒ (_p_ ⇒ _r_)) | _p_, _q_, _r_ ∈ _P_(_X_)}  
> A3 = {~~_p_ ⇒ _p_ | _p_ ∈ _P_(_X_)}  

We model this by saying that any set of theorems T is equal to T with any of these
extra axiomatic statements added to it.

    axiom (#A1) th(X, e) = th(X, th(impl(P, impl(Q, P)), e))
    axiom (#A2) th(X, e) = th(X, th(impl(impl(P, impl(Q, R)), impl(impl(P, Q), impl(P, R))), e))
    axiom (#A3) th(X, e) = th(X, th(impl(not(not(P)), P), e))

In addition, we have modus ponens ("from _p_ and _p_ ⇒ _q_, deduce _q_"):

    axiom (#MP) th(X, th(P, th(impl(P, Q), e))) = th(X, th(Q, th(P, th(impl(P, Q), e))))

I believe this is all we need to make this work.  So, let's pick a simple proof and write it up
and see if the `eqthy` checker can confirm it.  Example 4.5 on page 16 of Barnes and Mack:

>   ⊢ _p_ ⇒ _p_

We write this in equational logic by saying that any set of theorems is equal to a
set of theorems which contains this theorem.

Unfortunately, with the machinery that we've got so far, even though we
only care that the resulting set contains `impl(P, P)`, we show much more than
that -- we show all the intermediate results in getting there. So, we have to work
backwards -- removing the inetermediate results using the same axioms used to add
them -- for all the theorems except the desired theorem (`impl(P, P)`).

    theorem
        th(X, e) = th(X, th(impl(P, P), e))

The proof given in the book is

> p1 = p ⇒ ((p ⇒ p) ⇒ p)  [by A1]  
> p2 = (p ⇒ ((p ⇒ p) ⇒ p)) ⇒ ((p ⇒ (p ⇒ p)) ⇒ (p⇒p))  [by A2]  
> p3 = (p ⇒ (p ⇒ p)) ⇒ (p ⇒ p)  [p2 = p1 ⇒ p3]  
> p4 = p ⇒ (p ⇒ p)  [by A1]  
> p5 = p ⇒ p  [p3 = p4 ⇒ p5]  

And now we... mechanically translate that...

    proof
        th(X, e) = th(X, e)
        th(X, e) = th(X, th(impl(P, impl(Q, P)), e))                [by #A1]
        th(X, e) = th(X, th(impl(P, impl(impl(P, P), P)), e))       [by substitution of impl(P, P) into Q]

        th(X, e) = th(X, th(impl(P, impl(impl(P, P), P)),
                         th(impl(impl(P, impl(Q, R)), impl(impl(P, Q), impl(P, R))), e)))       [by #A2]

        th(X, e) = th(X, th(impl(P, impl(impl(P, P), P)),
                         th(impl(impl(P, impl(impl(P, P), R)), impl(impl(P, impl(P, P)), impl(P, R))), e)))
                                                                    [by substitution of impl(P, P) into Q]

        th(X, e) = th(X, th(impl(P, impl(impl(P, P), P)),
                         th(impl(impl(P, impl(impl(P, P), P)), impl(impl(P, impl(P, P)), impl(P, P))), e)))
                                                                    [by substitution of P into R]

        th(X, e) = th(X, th(impl(impl(P, impl(P, P)), impl(P, P)),
                         th(impl(P, impl(impl(P, P), P)),
                         th(impl(impl(P, impl(impl(P, P), P)), impl(impl(P, impl(P, P)), impl(P, P))), e))))
                                                                    [by #MP]

        th(X, e) = th(X, th(impl(impl(P, impl(P, P)), impl(P, P)),
                         th(impl(P, impl(impl(P, P), P)),
                         th(impl(impl(P, impl(impl(P, P), P)), impl(impl(P, impl(P, P)), impl(P, P))),
                         th(impl(P, impl(Q, P)), e)))))             [by #A1]

        th(X, e) = th(X, th(impl(impl(P, impl(P, P)), impl(P, P)),
                         th(impl(P, impl(impl(P, P), P)),
                         th(impl(impl(P, impl(impl(P, P), P)), impl(impl(P, impl(P, P)), impl(P, P))),
                         th(impl(P, impl(P, P)), e)))))             [by substitution of P into Q]

        th(X, e) = th(X, th(impl(P, impl(impl(P, P), P)),
                         th(impl(impl(P, impl(P, P)), impl(P, P)),
                         th(impl(impl(P, impl(impl(P, P), P)), impl(impl(P, impl(P, P)), impl(P, P))),
                         th(impl(P, impl(P, P)), e)))))
                                                                    [by #th-comm]

        th(X, e) = th(X, th(impl(P, impl(impl(P, P), P)),
                         th(impl(impl(P, impl(impl(P, P), P)), impl(impl(P, impl(P, P)), impl(P, P))),
                         th(impl(impl(P, impl(P, P)), impl(P, P)),
                         th(impl(P, impl(P, P)), e)))))
                                                                    [by #th-comm]

        th(X, e) = th(X, th(impl(P, impl(impl(P, P), P)),
                         th(impl(impl(P, impl(impl(P, P), P)), impl(impl(P, impl(P, P)), impl(P, P))),
                         th(impl(P, impl(P, P)),
                         th(impl(impl(P, impl(P, P)), impl(P, P)), e)))))
                                                                    [by #th-comm]

        th(X, e) = th(X, th(impl(P, impl(impl(P, P), P)),
                         th(impl(impl(P, impl(impl(P, P), P)), impl(impl(P, impl(P, P)), impl(P, P))),
                         th(impl(P, P),
                         th(impl(P, impl(P, P)),
                         th(impl(impl(P, impl(P, P)), impl(P, P)), e))))))
                                                                    [by #MP]

        th(X, e) = th(X, th(impl(P, impl(impl(P, P), P)),
                         th(impl(P, P),
                         th(impl(impl(P, impl(impl(P, P), P)), impl(impl(P, impl(P, P)), impl(P, P))),
                         th(impl(P, impl(P, P)),
                         th(impl(impl(P, impl(P, P)), impl(P, P)), e))))))
                                                                    [by #th-comm]

        th(X, e) = th(X, th(impl(P, P),
                         th(impl(P, impl(impl(P, P), P)),
                         th(impl(impl(P, impl(impl(P, P), P)), impl(impl(P, impl(P, P)), impl(P, P))),
                         th(impl(P, impl(P, P)),
                         th(impl(impl(P, impl(P, P)), impl(P, P)), e))))))
                                                                    [by #th-comm]

        th(X, e) = th(X, th(impl(P, P),
                         th(impl(P, impl(impl(P, P), P)),
                         th(impl(impl(P, impl(impl(P, P), P)), impl(impl(P, impl(P, P)), impl(P, P))),
                         th(impl(impl(P, impl(P, P)), impl(P, P)), 
                         th(impl(P, impl(P, P)), e))))))
                                                                    [by #th-comm]

        th(X, e) = th(X, th(impl(P, P),
                         th(impl(P, impl(impl(P, P), P)),
                         th(impl(impl(P, impl(impl(P, P), P)), impl(impl(P, impl(P, P)), impl(P, P))),
                         th(impl(impl(P, impl(P, P)), impl(P, P)), e)))))
                                                                    [by #A1]

        th(X, e) = th(X, th(impl(P, P),
                         th(impl(P, impl(impl(P, P), P)),
                         th(impl(impl(P, impl(P, P)), impl(P, P)),
                         th(impl(impl(P, impl(impl(P, P), P)), impl(impl(P, impl(P, P)), impl(P, P))), e)))))
                                                                    [by #th-comm]

        th(X, e) = th(X, th(impl(P, P),
                         th(impl(impl(P, impl(P, P)), impl(P, P)),
                         th(impl(P, impl(impl(P, P), P)),
                         th(impl(impl(P, impl(impl(P, P), P)), impl(impl(P, impl(P, P)), impl(P, P))), e)))))
                                                                    [by #th-comm]

        th(X, e) = th(X, th(impl(P, P),
                         th(impl(P, impl(impl(P, P), P)),
                         th(impl(impl(P, impl(impl(P, P), P)), impl(impl(P, impl(P, P)), impl(P, P))), e))))
                                                                    [by #MP]

        th(X, e) = th(X, th(impl(P, P),
                         th(impl(P, impl(impl(P, P), P)), e)))
                                                                    [by #A2]

        th(X, e) = th(X, th(impl(P, P), e))                         [by #A1]
    qed

[An Algebraic Introduction to Mathematical Logic]: https://archive.org/details/algebraicintrodu00barn_0
