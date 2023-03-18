from eqthy.objects import Reflexivity, Substitution, Congruence, Reference
from eqthy.terms import Eqn, all_rewrites, render, RewriteRule, replace, apply_substs_to_rule


class DerivationError(Exception):
    pass


class Verifier:
    def __init__(self, document, verbose=True, context=None):
        self.axioms = document.axioms
        self.theorems = document.theorems
        self.verbose = verbose
        self.context = context or {}
        self.rules = {}

        for axiom in self.axioms:
            self.register(axiom.name, axiom.eqn.lhs, axiom.eqn.rhs)

    def log(self, msg, *args):
        if self.verbose:
            print(msg.format(*args))

    def register(self, name, lhs, rhs):
        self.log("Registering rule [{}]: {} = {}", render(name), render(lhs), render(rhs))
        self.rules[name + '_1'] = RewriteRule(pattern=lhs, substitution=rhs)
        self.rules[name + '_2'] = RewriteRule(pattern=rhs, substitution=lhs)

    def verify(self):
        for theorem in self.theorems:
            self.verify_theorem(theorem)
            self.register(theorem.name, theorem.eqn.lhs, theorem.eqn.rhs)
        return self.context

    def verify_theorem(self, theorem):
        self.log("Verifying theorem [{}]: {}", render(theorem.name), render(theorem.eqn))
        prev = None
        rewritten_eqn = None
        eqn_shown = False
        for step_num, step in enumerate(theorem.steps):
            if prev is None:
                self.log("Verifying that {} follows from established rules", render(step.eqn))
                if step.eqn.lhs == step.eqn.rhs:
                    rewritten_eqn = step.eqn
                    self.log("Confirmed that {} follows from Reflexivity", render(step.eqn))
                else:
                    raise DerivationError("In step {} of {}: Could not derive {} from established rules".format(step_num + 1, theorem.name, render(step.eqn)))
            else:
                self.log("Verifying that {} follows from {}", render(step.eqn), render(prev.eqn))
                rewritten_eqn = self.obtain_rewritten_step(step, prev)
                if not rewritten_eqn:
                    raise DerivationError("In step {} of {}: Could not derive {} from {}".format(step_num + 1, theorem.name, render(step.eqn), render(prev.eqn)))

            if rewritten_eqn == theorem.eqn:
                self.log("With {} we have now shown the theorem {}".format(render(rewritten_eqn), render(theorem.eqn)))
                eqn_shown = True
            prev = step

        if not eqn_shown:
            raise DerivationError("No step in proof of {} showed {}".format(theorem.name, render(theorem.eqn)))

    def obtain_rewritten_step(self, step, prev):
        rules_to_try = self.rules
        if step.hint is not None:
            self.log("==> step has hint {}", step.hint)
            result = self.resolve_step_hint(step, prev)
            if result:
                return result
            result = self.narrow_rule_search(step)
            if result:
                rules_to_try = result

        # if no hint or hint resolution punted, search for rule to apply

        for (name, rule) in rules_to_try.items():
            self.log("  Trying to rewrite lhs {} with {}", render(prev.eqn.lhs), render(rule))
            for rewritten_lhs in all_rewrites(rule.pattern, rule.substitution, prev.eqn.lhs):
                self.log("    Using {}, rewrote {} to {}", render(rule), render(prev.eqn.lhs), render(rewritten_lhs))
                rewritten_eqn = Eqn(rewritten_lhs, prev.eqn.rhs)
                if step.eqn == rewritten_eqn:
                    self.log("    Can rewrite lhs to obtain: {}", render(rewritten_eqn))
                    return rewritten_eqn

            self.log("  Trying to rewrite rhs {} with {}", render(prev.eqn.rhs), render(rule))
            for rewritten_rhs in all_rewrites(rule.pattern, rule.substitution, prev.eqn.rhs):
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

    def narrow_rule_search(self, step):
        if isinstance(step.hint, Reference):
            if step.hint.name + '_1' not in self.rules:
                raise DerivationError("Rule named {} has not been established".format(step.hint.name))
            rules = {}
            rules[step.hint.name + '_1'] = apply_substs_to_rule(self.rules[step.hint.name + '_1'], step.hint.substs)
            rules[step.hint.name + '_2'] = apply_substs_to_rule(self.rules[step.hint.name + '_2'], step.hint.substs)
            return rules
