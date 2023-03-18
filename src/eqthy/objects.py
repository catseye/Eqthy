"""Objects in the Eqthy document structure."""
from collections import namedtuple

Document = namedtuple('Document', ['axioms', 'theorems'])
Axiom = namedtuple('Axiom', ['name', 'eqn'])
Theorem = namedtuple('Theorem', ['name', 'eqn', 'steps'])
Step = namedtuple('Step', ['eqn', 'hint'])

# hints

Reflexivity = namedtuple('Reflexivity', [])
Substitution = namedtuple('Substitution', ['term', 'variable'])
Congruence = namedtuple('Congruence', ['variable', 'term'])
Reference = namedtuple('Reference', ['name', 'side', 'substs'])
