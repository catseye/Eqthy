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

Some basic lemmas, leading up to, we hope, a proof of de Morgan's laws.
For the most part, these follow the lemmas given in
[this stackexchange answer](https://math.stackexchange.com/a/95884) by Arturo Magidin.
However, since some of those lemmas rely on properties that are not proved there,
other lemmas were adapted from the other sources, including
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

     theorem (#and-annihil)
        and(A, 0) = 0
     proof
        0 = 0
        and(A, not(A)) = 0
        and(and(A, A), not(A)) = 0
        and(A, and(A, not(A))) = 0
        and(A, 0) = 0
     qed

     theorem
        and(and(A, B), or(not(A), not(B))) = 0
     proof
        0 = 0
        or(0, 0) = 0
        or(0, and(A, 0)) = 0
        or(and(B, 0), and(A, 0)) = 0                                [by #and-annihil with A=B]
        or(and(0, B), and(A, 0)) = 0
        or(and(and(A, not(A)), B), and(A, 0)) = 0
        or(and(and(not(A), A), B), and(A, 0)) = 0
        or(and(not(A), and(A, B)), and(A, 0)) = 0
        or(and(and(A, B), not(A)), and(A, 0)) = 0
        or(and(and(A, B), not(A)), and(A, and(B, not(B)))) = 0      [by #and-comp with A=B]
        or(and(and(A, B), not(A)), and(and(A, B), not(B))) = 0
        and(and(A, B), or(not(A), not(B))) = 0
     qed
