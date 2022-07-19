from eqthy.terms import all_matches, render
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
        self.log("Verifying theorem {}", render(theorem.eqn))
        prev = None
        for step in theorem.steps:
            if prev is None:
                self.log("Confirming that {} follows from established rules", render(step))
                if step.lhs == step.rhs:
                    self.log("Confirmed that {} follows from Reflexivity", render(step))
                else:
                    raise DerivationError("Cannot derive {} from established rules".format(render(step)))
            else:
                self.log("Confirming that {} follows from {}", render(step), render(prev))
                raise DerivationError("Cannot derive {} from {}".format(render(step), render(prev)))
            prev = step
