from eqthy.terms import Eqn, all_matches, subst, render, RewriteRule


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
        eqn_shown = False
        for step in theorem.steps:
            if prev is None:
                self.log("Verifying that {} follows from established rules", render(step))
                if step.lhs == step.rhs:
                    self.log("Confirmed that {} follows from Reflexivity", render(step))
                else:
                    raise DerivationError("Could not derive {} from established rules".format(render(step)))
            else:
                self.log("Verifying that {} follows from {}", render(step), render(prev))
                rewritten_step = self.obtain_rewritten_step(step, prev)
                if not rewritten_step:
                    raise DerivationError("Could not derive {} from {}".format(render(step), render(prev)))

            if step == theorem.eqn:
                eqn_shown = True
            prev = step

        if not eqn_shown:
            raise DerivationError("No step in proof showed {}".format(render(theorem.eqn)))

    def obtain_rewritten_step(self, step, prev):
        # TODO: if name of rule given, use that rule only
        for rule in self.rules:
            self.log("  Trying to rewrite lhs {} with {}", render(prev.lhs), render(rule))
            for rewritten_lhs in self.all_rewrites(rule, prev.lhs):
                rewritten_step = Eqn(rewritten_lhs, prev.rhs)
                if step == rewritten_step:
                    self.log("    Can rewrite lhs to obtain: {}", render(rewritten_step))
                    return rewritten_step

            self.log("  Trying to rewrite rhs {} with {}", render(prev.rhs), render(rule))
            for rewritten_rhs in self.all_rewrites(rule, prev.rhs):
                rewritten_step = Eqn(prev.lhs, rewritten_rhs)
                if step == rewritten_step:
                    self.log("    Can rewrite rhs to obtain: {}", render(rewritten_step))
                    return rewritten_step

    def all_rewrites(self, rule, term):
        matches = all_matches(rule.pattern, term)
        self.log("    Matches: {}", matches)
        rewrites = []
        for (index, unifier) in matches:
            rewrites.append(subst(rule.substitution, unifier))
        return rewrites
