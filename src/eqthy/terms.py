from copy import copy
from collections import namedtuple


Term = namedtuple('Term', ['ctor', 'subterms'])
Variable = namedtuple('Variable', ['name'])
Eqn = namedtuple('Eqn', ['lhs', 'rhs'])
RewriteRule = namedtuple('RewriteRule', ['pattern', 'substitution'])

Unifier = namedtuple('Unifier', ['success', 'bindings'])


unify_fail = Unifier(success=False, bindings={})


def render(t):
    if isinstance(t, Term):
        if t.subterms:
            return "{}({})".format(t.ctor, ', '.join([render(st) for st in t.subterms]))
        else:
            return t.ctor
    elif isinstance(t, Variable):
        return t.name
    elif isinstance(t, Eqn):
        return "{} = {}".format(render(t.lhs), render(t.rhs))
    elif isinstance(t, RewriteRule):
        return "{} => {}".format(render(t.pattern), render(t.substitution))
    elif isinstance(t, Unifier):
        if not t.success:
            return '#F'
        else:
            return str(dict([(k, render(v)) for k, v in t.bindings.items()]))
    else:
        return str(t)


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
            return unify_fail
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
    if unifier.success:
        matches.append((index, unifier))

    if isinstance(term, Term):
        for n, subterm in enumerate(term.subterms):
            matches += all_matches(pattern, subterm, index + [n])

    return matches


def expand(term, unifier):
    if not unifier.success:
        return term
    elif isinstance(term, Variable):
        if term.name in unifier.bindings:
            return unifier.bindings[term.name]
        else:
            return term
    elif isinstance(term, Term):
        return Term(term.ctor, [expand(st, unifier) for st in term.subterms])
    else:
        raise NotImplementedError(str(term))


def subterm_at_index(term, index):
    if not index:
        return term
    elif isinstance(term, Term):
        position = index[0]
        return subterm_at_index(term.subterms[position], index[1:])
    else:
        raise KeyError('{} at {}'.format(str(term), index))


def update_at_index(term, subterm, index):
    if not index:
        return subterm
    elif isinstance(term, Term):
        position = index[0]
        replaced_subterm = update_at_index(term.subterms[position], subterm, index[1:])
        new_subterms = copy(term.subterms)
        new_subterms[position] = replaced_subterm
        return Term(term.ctor, new_subterms)
    else:
        raise KeyError('{} at {}'.format(str(term), index))


def replace(term, target, replacement):
    if term == target:
        return replacement
    elif isinstance(term, Term):
        return Term(term.ctor, [replace(st, target, replacement) for st in term.subterms])
    else:
        return term


def all_rewrites(pattern, substitution, term):
    """Given a rule (a pattern and a substitution) and a term, return
    a list of the terms that would result from rewriting the term
    in all the possible ways by the rule."""

    # First, obtain all the unifiers where the pattern of the rule matches any subterm of the term
    matches = all_matches(pattern, term)

    # Now, collect all the rewritten terms -- a subterm replaced by the expanded rhs of the rule
    rewrites = []
    for (index, unifier) in matches:
        rewritten_subterm = expand(substitution, unifier)
        result = update_at_index(term, rewritten_subterm, index)
        rewrites.append(result)

    return rewrites
