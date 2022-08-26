from eqthy.terms import all_matches, subst, render, RewriteRule
from collections import namedtuple


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
                self.log("Verifying that {} follows from established rules", render(step))
                if step.lhs == step.rhs:
                    self.log("Confirmed that {} follows from Reflexivity", render(step))
                else:
                    raise DerivationError("Could not derive {} from established rules".format(render(step)))
            else:
                self.log("Verifying that {} follows from {}", render(step), render(prev))

                # TODO: if name of rule given, use that rule only
                rewritten_lhs = None
                for rule in self.rules:
                    self.log("  Trying to rewrite {} with {}", render(prev.lhs), render(rule))
                    rewrites = self.all_rewrites(rule, prev.lhs)
                    if rewrites:
                        for rewrite in rewrites:
                            self.log("    Can rewrite to {}", render(rewrite))
                        # rewritten_lhs = result
                        # break
                if not rewritten_lhs:
                    raise DerivationError("Could not derive {} from {}".format(render(step), render(prev)))

            prev = step

    def all_rewrites(self, rule, term):
        matches = all_matches(rule.pattern, term)
        self.log("    Matches: {}", matches)
        rewrites = []
        for (index, unifier) in matches:
            rewrites += subst(term, unifier)
        return rewrites
