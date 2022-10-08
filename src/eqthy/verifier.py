# TODO: these should probably come from a "eqthy.hints" module
from eqthy.parser import Substitution, Congruence
from eqthy.terms import Eqn, all_matches, subst, render, RewriteRule


class DerivationError(Exception):
    pass


class Verifier:
    def __init__(self, development, verbose=True):
        self.axioms = development.axioms
        self.theorems = development.theorems
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
        eqn_shown = False
        for step in theorem.steps:
            if prev is None:
                self.log("Verifying that {} follows from established rules", render(step.eqn))
                if step.eqn.lhs == step.eqn.rhs:
                    self.log("Confirmed that {} follows from Reflexivity", render(step.eqn))
                else:
                    raise DerivationError("Could not derive {} from established rules".format(render(step.eqn)))
            else:
                self.log("Verifying that {} follows from {}", render(step.eqn), render(prev.eqn))
                if not self.obtain_rewritten_step(step, prev):
                    raise DerivationError("Could not derive {} from {}".format(render(step.eqn), render(prev.eqn)))

            if step.eqn == theorem.eqn:
                eqn_shown = True
            prev = step

        if not eqn_shown:
            raise DerivationError("No step in proof showed {}".format(render(theorem.eqn)))

    def obtain_rewritten_step(self, step, prev):
        if step.hint:
            if isinstance(step.hint, Substitution):
                raise NotImplementedError(step.hint)
            elif isinstance(step.hint, Congruence):
                raise NotImplementedError(step.hint)
            else:
                # TODO we can only check that this hint is not inaccurate
                self.log("==> step has unacted-upon hint {}", step.hint)
        for rule in self.rules:
            self.log("  Trying to rewrite lhs {} with {}", render(prev.eqn.lhs), render(rule))
            for rewritten_lhs in self.all_rewrites(rule, prev.eqn.lhs):
                rewritten_eqn = Eqn(rewritten_lhs, prev.eqn.rhs)
                if step.eqn == rewritten_eqn:
                    self.log("    Can rewrite lhs to obtain: {}", render(rewritten_eqn))
                    return rewritten_eqn

            self.log("  Trying to rewrite rhs {} with {}", render(prev.eqn.rhs), render(rule))
            for rewritten_rhs in self.all_rewrites(rule, prev.eqn.rhs):
                rewritten_eqn = Eqn(prev.eqn.lhs, rewritten_rhs)
                if step.eqn == rewritten_eqn:
                    self.log("    Can rewrite rhs to obtain: {}", render(rewritten_eqn))
                    return rewritten_eqn

    def all_rewrites(self, rule, term):
        matches = all_matches(rule.pattern, term)
        rewrites = []
        for (index, unifier) in matches:
            rewrites.append(subst(rule.substitution, unifier))
        return rewrites
