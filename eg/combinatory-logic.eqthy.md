Combinatory Logic
=================

For more information, see, for example, [Combinatory Logic on Wikipedia](https://en.wikipedia.org/wiki/Combinatory_logic)
or [Combinatory Logic on SEP](https://plato.stanford.edu/entries/logic-combinatory/).

Only three axioms are needed.  Unfortunately, the case of the symbols is the
opposite of most expositions: combinators are lower-case letters, while
variable names are capitals.

    axiom app(i, X) = X
    axiom app(app(k, X), Y) = X
    axiom app(app(app(s, X), Y), Z) = app(app(X, Z), app(Y, Z))

Proof that SKK does the same thing as I.

    theorem
        app(app(app(s, k), k), X) = X
    proof
        X = X
        app(app(k, X), Y) = X
        app(app(k, X), app(k, X)) = X   [by substitution of app(k, X) into Y]
        app(app(app(s, k), k), X) = X
    qed
