History of Eqthy
================

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
