# TODO: these should probably come from a "eqthy.hints" module
from eqthy.parser import Reflexivity, Substitution, Congruence
from eqthy.terms import Eqn, all_matches, expand, subterm_at_index, update_at_index, render, RewriteRule, replace


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
        rewritten_eqn = None
        eqn_shown = False
        for step in theorem.steps:
            if prev is None:
                self.log("Verifying that {} follows from established rules", render(step.eqn))
                if step.eqn.lhs == step.eqn.rhs:
                    rewritten_eqn = step.eqn
                    self.log("Confirmed that {} follows from Reflexivity", render(step.eqn))
                else:
                    raise DerivationError("Could not derive {} from established rules".format(render(step.eqn)))
            else:
                self.log("Verifying that {} follows from {}", render(step.eqn), render(prev.eqn))
                rewritten_eqn = self.obtain_rewritten_step(step, prev)
                if not rewritten_eqn:
                    raise DerivationError("Could not derive {} from {}".format(render(step.eqn), render(prev.eqn)))

            if rewritten_eqn == theorem.eqn:
                self.log("With {} we have now shown the theorem {}".format(render(rewritten_eqn), render(theorem.eqn)))
                eqn_shown = True
            prev = step

        if not eqn_shown:
            raise DerivationError("No step in proof showed {}".format(render(theorem.eqn)))

    def obtain_rewritten_step(self, step, prev):
        if step.hint is not None:
            self.log("==> step has hint {}", step.hint)
            result = self.resolve_step_hint(step, prev)
            if result:
                return result

        # if no hint or hint resolution punted, search for rule to apply

        for rule in self.rules:
            self.log("  Trying to rewrite lhs {} with {}", render(prev.eqn.lhs), render(rule))
            for rewritten_lhs in self.all_rewrites(rule, prev.eqn.lhs):
                self.log("    Using {}, rewrote {} to {}", render(rule), render(prev.eqn.lhs), render(rewritten_lhs))
                rewritten_eqn = Eqn(rewritten_lhs, prev.eqn.rhs)
                if step.eqn == rewritten_eqn:
                    self.log("    Can rewrite lhs to obtain: {}", render(rewritten_eqn))
                    return rewritten_eqn

            self.log("  Trying to rewrite rhs {} with {}", render(prev.eqn.rhs), render(rule))
            for rewritten_rhs in self.all_rewrites(rule, prev.eqn.rhs):
                self.log("    Using {}, rewrote {} to {}", render(rule), render(prev.eqn.rhs), render(rewritten_rhs))
                rewritten_eqn = Eqn(prev.eqn.lhs, rewritten_rhs)
                if step.eqn == rewritten_eqn:
                    self.log("    Can rewrite rhs to obtain: {}", render(rewritten_eqn))
                    return rewritten_eqn

    def resolve_step_hint(self, step, prev):
        if isinstance(step.hint, Substitution):
            # replace all occurrences of variable in step with term
            rewritten_eqn = Eqn(
                replace(prev.eqn.lhs, step.hint.variable, step.hint.term),
                replace(prev.eqn.rhs, step.hint.variable, step.hint.term)
            )
            self.log("  Rewrote {} with Substitution to obtain: {}", render(prev.eqn), render(rewritten_eqn))
            if rewritten_eqn != step.eqn:
                raise DerivationError("Substitution did not result in {}".format(render(step.eqn)))
            return rewritten_eqn
        elif isinstance(step.hint, Congruence):
            # replace all occurrences of variable in hint with step
            rewritten_eqn = Eqn(
                replace(step.hint.term, step.hint.variable, prev.eqn.lhs),
                replace(step.hint.term, step.hint.variable, prev.eqn.rhs)
            )
            self.log("  Rewrote {} with Congruence to obtain: {}", render(prev.eqn), render(rewritten_eqn))
            if rewritten_eqn != step.eqn:
                raise DerivationError("Congruence did not result in {}".format(render(step.eqn)))
            return rewritten_eqn
        elif isinstance(step.hint, Reflexivity):
            if step.eqn.lhs == step.eqn.rhs:
                return step.eqn
            else:
                raise DerivationError("Could not derive {} from Reflexivity".format(render(step.eqn)))
        else:
            # TODO do other checking on this hint instead of ignoring it
            self.log("==> step has unacted-upon hint {}", step.hint)

    def all_rewrites(self, rule, term):
        """Given a term, and a rule, return a list of the terms that would result
        from rewriting the term in all the possible ways by the rule."""

        # First, obtain all the unifiers where the pattern of the rule matches any subterm of the term
        matches = all_matches(rule.pattern, term)

        # Now, collect all the rewritten terms -- a subterm replaced by the expanded rhs of the rule
        rewrites = []
        for (index, unifier) in matches:
            rewritten_subterm = expand(rule.substitution, unifier)
            result = update_at_index(term, rewritten_subterm, index)
            rewrites.append(result)

        return rewrites
