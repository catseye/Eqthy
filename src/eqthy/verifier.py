from eqthy.terms import all_matches
from collections import namedtuple

RewriteRule = namedtuple('RewriteRule', ['pattern', 'substitution'])


class DerivationError(Exception):
    pass


class Verifier:
    def __init__(self, program, verbose=True):
        self.axioms = program.axioms
        self.theorems = program.theorems
        self.verbose = verbose
        self.rules = []

        for axiom in self.axioms:
            lhs = axiom.eqn.lhs
            rhs = axiom.eqn.rhs
            self.rules.append(RewriteRule(pattern=lhs, substitution=rhs))
            self.rules.append(RewriteRule(pattern=rhs, substitution=lhs))

    def log(self, msg, *args):
        if self.verbose:
            print(msg.format(*args))

    def verify(self):
        for theorem in self.theorems:
            self.verify_theorem(theorem)
            lhs = theorem.eqn.lhs
            rhs = theorem.eqn.rhs
            self.rules.append(RewriteRule(pattern=lhs, substitution=rhs))
            self.rules.append(RewriteRule(pattern=rhs, substitution=lhs))

    def verify_theorem(self, theorem):
        self.log("Verifying theorem {}", theorem)
        prev = None
        for step in theorem.steps:
            self.log("Confirming that {} follows from {}", step, prev)
            prev = step
        raise DerivationError("Cannot derive {} from {}".format(step, prev))
