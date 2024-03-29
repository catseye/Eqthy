from eqthy.objects import (
    Document, Axiom, Theorem, Step,
    Reflexivity, Substitution, Congruence, Reference
)
from eqthy.scanner import Scanner, EqthySyntaxError
from eqthy.terms import Term, Variable, Eqn


# Document := {Axiom} {Theorem}.
# Axiom    := "axiom" [Name] Eqn.
# Theorem  := "theorem" [Name] Eqn "proof" {Step} "qed".
# Name     := "(" Ident ")".
# Step     := Eqn ["[" "by" Hint "]"].
# Hint     := "reflexivity"
#           | "substitution" "of" Term "into" Var
#           | "congruence" "of" Var "and" Term
#           | Ident ["on" ("LHS" | "RHS")] ["with" Subst {"," Subst}].
# Eqn      := Term "=" Term.
# Term     := Var | Ctor ["(" [Term {"," Term} ")"].


class Parser(object):
    def __init__(self, text, filename):
        self.scanner = Scanner(text, filename)
        self.axiom_count = 0
        self.theorem_count = 0

    def document(self):
        axioms = []
        theorems = []
        while self.scanner.on('axiom'):
            axioms.append(self.axiom())
        while self.scanner.on('theorem'):
            theorems.append(self.theorem())
        if not (axioms or theorems):
            raise EqthySyntaxError(
                self.scanner.filename,
                self.scanner.line_number,
                "Eqthy document is empty"
            )
        return Document(axioms=axioms, theorems=theorems)

    def axiom(self):
        self.scanner.expect('axiom')
        name = self.name()
        eqn = self.eqn()
        if not name:
            self.axiom_count += 1
            name = 'unnamed_axiom_{}'.format(self.axiom_count)
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
        if not name:
            self.theorem_count += 1
            name = 'unnamed_theorem_{}'.format(self.theorem_count)
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
            return Reflexivity()
        elif self.scanner.consume('substitution'):
            self.scanner.expect('of')
            term = self.term()
            self.scanner.expect('into')
            variable = self.var()
            return Substitution(term=term, variable=variable)
        elif self.scanner.consume('congruence'):
            self.scanner.expect('of')
            variable = self.var()
            self.scanner.expect('and')
            term = self.term()
            return Congruence(term=term, variable=variable)
        else:
            name = self.scanner.token
            side = None
            substs = []
            self.scanner.scan()
            if self.scanner.consume('on'):
                if self.scanner.on('LHS') or self.scanner.on('RHS'):
                    side = self.scanner.token
                    self.scanner.scan()
                else:
                    self.scanner.syntax_error("Expected 'LHS' or 'RHS'")
            if self.scanner.consume('with'):
                substs.append(self.eqn())
                while self.scanner.consume(','):
                    substs.append(self.eqn())
            return Reference(name=name, side=side, substs=substs)

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

    def var(self):
        var = self.term()
        if not isinstance(var, Variable):
            self.scanner.syntax_error("Expected variable")
        return var
