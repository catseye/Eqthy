from copy import copy
from collections import namedtuple


Term = namedtuple('Term', ['ctor', 'subterms'])
Variable = namedtuple('Variable', ['name'])

Unifier = namedtuple('Unifier', ['success', 'bindings'])


unify_fail = Unifier(success=False, bindings={})


def merge_unifiers(first, next):
    if not first.success or not next.success:
        return unify_fail
    bindings = copy(first.bindings)
    for key, value in next.bindings.items():
        if key in bindings and bindings[key] != value:
            return unify_fail
        bindings[key] = value
    return Unifier(success=True, bindings=bindings)


def match(pattern, term):
    if isinstance(pattern, Variable):
        return Unifier(success=True, bindings={
            pattern.name: term
        })
    else:
        assert isinstance(pattern, Term)
        if not isinstance(term, Term) or len(term.subterms) != len(pattern.subterms):
            return False
        unifier = Unifier(success=True, bindings={})
        for (subpattern, subterm) in zip(pattern.subterms, term.subterms):
            subunifier = match(subpattern, subterm)
            unifier = merge_unifiers(unifier, subunifier)
        return unifier


def all_matches(pattern, term, index=None):
    if index is None:
        index = []

    matches = []

    unifier = match(pattern, term)
    matches.append((index, unifier))

    for n, subterm in enumerate(term.subterms):
        matches += all_matches(pattern, subterm, index + [n])

    return matches
