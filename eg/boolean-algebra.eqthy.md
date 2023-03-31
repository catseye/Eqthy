Boolean Algebra
===============

For more information, see
[Boolean algebra (structure)](https://en.wikipedia.org/wiki/Boolean_algebra_(structure)) on Wikipedia.

    axiom (#or-assoc)       or(A, or(B, C)) = or(or(A, B), C)
    axiom (#or-comm)        or(A, B) = or(B, A)
    axiom (#or-absorp)      or(A, and(A, B)) = A
    axiom (#or-dist)        or(A, and(B, C)) = and(or(A, B), or(A, C))
    axiom (#or-comp)        or(A, not(A)) = 1
    axiom (#and-assoc)      and(A, and(B, C)) = and(and(A, B), C)
    axiom (#and-comm)       and(A, B) = and(B, A)
    axiom (#and-absorp)     and(A, or(A, B)) = A
    axiom (#and-dist)       and(A, or(B, C)) = or(and(A, B), and(A, C))
    axiom (#and-comp)       and(A, not(A)) = 0

We'll now establish some basic lemmas based on these axioms.
These in turn could, in another setting, provide support for
a proof of De Morgan's Laws.  In this purely equational setting though,
for reasons I'll explain below, we won't actually be able to give
a proof De Morgan's Laws using them.  Still, the lemmas
are instructive, could be useful for other proofs, and serve
the point of exercising the Eqthy language and its proof-checkers.

For the most part, these follow the lemmas given in
[this stackexchange answer](https://math.stackexchange.com/a/95884) by Arturo Magidin
and, where those are lacking,
[this stackexchange answer](https://math.stackexchange.com/a/2111450) by Kanwaljit Singh.

    theorem (#or-ident)
        or(X, 0) = X
    proof
        X = X
        or(X, and(X, not(X))) = X         [by #or-absorp with B=not(X)]
        or(X, 0) = X                      [by #and-comp]
    qed

    theorem (#and-ident)
        and(X, 1) = X
    proof
        X = X
        and(X, or(X, not(X))) = X         [by #and-absorp with B=not(X)]
        and(X, 1) = X                     [by #or-comp]
    qed

    theorem (#or-idemp)
        or(X, X) = X
    proof
        X = X
        or(X, 0) = X
        or(X, and(X, not(X))) = X             [by #and-comp with A=X]
        and(or(X, X), or(X, not(X))) = X
        and(or(X, X), 1) = X
        or(X, X) = X
    qed

    theorem (#and-idemp)
        and(X, X) = X
    proof
        X = X
        and(X, 1) = X
        and(X, or(X, not(X))) = X             [by #or-comp with A=X]
        or(and(X, X), and(X, not(X))) = X
        or(and(X, X), 0) = X
        and(X, X) = X
    qed

    theorem (#or-annihil)
        or(X, 1) = 1
    proof
        1 = 1
        or(X, not(X)) = 1                     [by #or-comp with A=X]
        or(or(X, X), not(X)) = 1
        or(X, or(X, not(X))) = 1
        or(X, 1) = 1
    qed

    theorem (#and-annihil)
        and(X, 0) = 0
    proof
        0 = 0
        and(X, not(X)) = 0                     [by #and-comp with A=X]
        and(and(X, X), not(X)) = 0
        and(X, and(X, not(X))) = 0
        and(X, 0) = 0
    qed

    theorem
        and(and(A, B), or(not(A), not(B))) = 0
    proof
        0 = 0
        or(0, 0) = 0
        or(0, and(A, 0)) = 0                                        [by #and-annihil with X=A]
        or(and(B, 0), and(A, 0)) = 0                                [by #and-annihil with X=B]
        or(and(0, B), and(A, 0)) = 0
        or(and(and(A, not(A)), B), and(A, 0)) = 0
        or(and(and(not(A), A), B), and(A, 0)) = 0
        or(and(not(A), and(A, B)), and(A, 0)) = 0
        or(and(and(A, B), not(A)), and(A, 0)) = 0
        or(and(and(A, B), not(A)), and(A, and(B, not(B)))) = 0      [by #and-comp with A=B]
        or(and(and(A, B), not(A)), and(and(A, B), not(B))) = 0
        and(and(A, B), or(not(A), not(B))) = 0
    qed

    theorem
        or(and(A, B), or(not(A), not(B))) = 1
    proof
        1 = 1
        or(not(A), 1) = 1                          [by #or-annihil with X=not(A)]
        or(1, not(A)) = 1
        or(or(B, not(B)), not(A)) = 1              [by #or-comp with A=B]
        or(or(not(B), B), not(A)) = 1
        or(not(B), or(B, not(A))) = 1
        or(or(B, not(A)), not(B)) = 1
        or(and(or(B, not(A)), 1), not(B)) = 1
        or(and(1, or(B, not(A))), not(B)) = 1
        or(and(1, or(not(A), B)), not(B)) = 1
        or(    and(or(A, not(A)), or(not(A), B)),     not(B)) = 1
        or(    and(or(A, not(A)), or(B, not(A))),     not(B)) = 1
        or(    and(or(not(A), A), or(B, not(A))),     not(B)) = 1
        or(    and(or(not(A), A), or(not(A), B)),     not(B)) = 1
        or(    or(not(A), and(A, B)),                 not(B)) = 1       [by #or-dist]
        or(    or(and(A, B), not(A)),                 not(B)) = 1
        or(and(A, B), or(not(A), not(B))) = 1
    qed

Unfortunately, the remaining step that Arturo Magidin gives (essentially
following Huntington's 1904 approach), which is basically

>     From
>       and(and(A, B), or(not(A), not(B))) = 0
>     and
>       or(and(A, B), or(not(A), not(B))) = 1
>     infer
>       not(and(A, B)) = or(not(A), not(B))

is not expressible in equational logic, so can't be written in Eqthy.
This is why I said above that we would not be able to follow this
path of lemmas all the way to a proof of De Morgan's Laws.

(There _is_ a purely equational proof of De Morgan's Laws; I know this
because I asked the E prover to find one, and it did so.  I would
need to translate it into Eqthy to include it here, and I haven't
done so yet.  I also don't know yet how much similarity it bears to
Huntington's approach.)

In the meantime however, we can state a couple of other potentially
useful lemmas involving `not`.

    theorem
        not(1) = 0
    proof
        0 = 0
        and(A, not(A)) = 0
        and(1, not(1)) = 0      [by substitution of 1 into A]
        and(not(1), 1) = 0
        not(1) = 0
    qed

    theorem
        not(0) = 1
    proof
        1 = 1
        or(A, not(A)) = 1
        or(0, not(0)) = 1      [by substitution of 0 into A]
        or(not(0), 0) = 1
        not(0) = 1
    qed

    theorem
        not(not(A)) = A
    proof
        1 = 1
        1 = or(A, not(A))
        1 = or(not(A), A)
        or(not(not(A)), 1) = or(not(not(A)), or(not(A), A))     [by congruence of X and or(not(not(A)), X)]
        not(not(A)) = or(not(not(A)), or(not(A), A))
        not(not(A)) = or(or(not(not(A)), not(A)), A)
        not(not(A)) = or(or(not(A), not(not(A))), A)
        not(not(A)) = or(1, A)
        not(not(A)) = or(A, 1)
        not(not(A)) = A
    qed
