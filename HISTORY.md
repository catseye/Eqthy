History of Eqthy
================

0.3
---

Implementation:

*   A bug where two terms could unify even though they have
    different constructors was discovered and fixed by
    Proloy Mishra (@pro465), who also repaired the proof in
    `boolean-algebra.eqthy.md` that had passed checking
    only due to this bug.
*   Slightly improved logging produced in `--verbose` mode.

Distribution:

*   The axiom system used in `propositional-algebra.eqthy.md`
    was identified to be inconsistent, also by @pro465.  The
    axiom was replaced with one that is probably not
    inconsistent, and the proof was repaired (although not
    in a particularly satisfying way -- the whole thing could
    stand to be done in a simpler way, if possible).

0.2
---

Language:

*   Added support for `with` clause in `by` hints, allowing
    variables in the axiom or previously-proved theorem to
    be renamed before applying it to the current step.

Implementation:

*   When there is a derivation error, the name of the theorem,
    and the step number within that theorem, are now included in
    the error message.
*   Refactored and cleaned up (`flake8`) the code in small ways.

Distribution:

*   Simplified the proof in the Propositional Algebra document.
*   Added example documents containing proofs in Boolean Algebra
    and Combinatory Logic.
*   Added a few more proofs in group theory, involving inverses.
*   Added example documents demonstrating `with` and demonstrating
    using a previously-proved theorem in a step.
*   Added this `HISTORY.md` file.

0.1
---

Initial release.
