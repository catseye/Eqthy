from collections import namedtuple

from eqthy.scanner import Scanner
from eqthy.terms import Term, Variable, Eqn


# Development := {Axiom} {Theorem}.
# Axiom   := "axiom" [Name] Eqn.
# Theorem := "theorem" [Name] Eqn "proof" {Step} "qed".
# Name    := "(" Ident ")".
# Step    := Eqn ["[" "by" Hint "]"].
# Hint    := "reflexivity"
#          | "substitution" "of" Term "into" Term
#          | "congruence" "of" Term "and" Term
#          | Ident ["on" ("LHS" | "RHS")].
# Eqn     := Term "=" Term.
# Term    := Var | Ctor ["(" [Term {"," Term} ")"].


Development = namedtuple('Development', ['axioms', 'theorems'])
Axiom = namedtuple('Axiom', ['name', 'eqn'])
Theorem = namedtuple('Theorem', ['name', 'eqn', 'steps'])
Step = namedtuple('Step', ['eqn', 'hint'])


class Parser(object):
    def __init__(self, text, filename):
        self.scanner = Scanner(text, filename)

    def development(self):
        axioms = []
        theorems = []
        while self.scanner.on('axiom'):
            axioms.append(self.axiom())
        while self.scanner.on('theorem'):
            theorems.append(self.theorem())
        return Development(axioms=axioms, theorems=theorems)

    def axiom(self):
        self.scanner.expect('axiom')
        name = self.name()
        eqn = self.eqn()
        return Axiom(name=name, eqn=eqn)

    def theorem(self):
        self.scanner.expect('theorem')
        name = self.name()
        eqn = self.eqn()
        self.scanner.expect('proof')
        steps = []
        while not self.scanner.on('qed'):
            steps.append(self.step())
        self.scanner.expect('qed')
        return Theorem(name=name, eqn=eqn, steps=steps)

    def name(self):
        if self.scanner.consume('('):
            ident = self.scanner.token
            self.scanner.scan()
            self.scanner.expect(')')
            return ident
        else:
            return None

    def step(self):
        eqn = self.eqn()
        if self.scanner.consume('['):
            self.scanner.expect('by')
            hint = self.hint()
            self.scanner.expect(']')
        else:
            hint = None
        return Step(eqn=eqn, hint=hint)

    def hint(self):
        if self.scanner.consume('reflexivity'):
            return ("reflexivity",)
        else:
            raise NotImplementedError()

    def eqn(self):
        lhs = self.term()
        self.scanner.expect('=')
        rhs = self.term()
        return Eqn(lhs=lhs, rhs=rhs)

    def term(self):
        name = self.scanner.token
        self.scanner.scan()
        if name.isupper():
            return Variable(name=name)
        subterms = []
        if self.scanner.consume('('):
            while not self.scanner.on(')'):
                subterms.append(self.term())
                if not self.scanner.on(')'):
                    self.scanner.expect(',')
            self.scanner.expect(')')
        return Term(ctor=name, subterms=subterms)
