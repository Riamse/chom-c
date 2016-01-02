#!/usr/bin/python

# TODO: add Context objects for blocks and variables and stuff.

import sys
import collections

from common import Data

TWO_ZILLION = (2 ** 30 - 1) * 2 + 1

sys.setrecursionlimit(2 ** 10)


class ProbabilityDistribution:
    def __init__(self, name="X"):
        self.name = name
        self.crapmap = {}
        self.rvcrapmap = {}
        self.crap = {}

    def __repr__(self):
        return "{.__name__}(name={!r})".format(type(self), self.name)

    def _behasherise(self, crap):
        v = hash(crap) % TWO_ZILLION
        if v in self.rvcrapmap:
            return self._behasherise(str(v))
        return v

    def __setitem__(self, val, p):
        h = self.crapmap.get(val, self._behasherise(val))
        self.crapmap[val] = h
        self.rvcrapmap[h] = val
        self.crap[h] = p

    def __getitem__(self, val):
        # returns P(X = val) for a rv X st X ~ self
        return self.crap[val]

    def __call__(self, n=1):
        #if sum(self.crap.values()) != 1:
        #    raise TypeError("not a real distribution")
        garbage = [], []
        for k, v in self.crap.items():
            garbage[0].append(k)
            garbage[1].append(v)
        from scipy.stats import rv_discrete  # overkill, yo
        X = rv_discrete(values=garbage)
        realret = [None] * n
        for i, h in enumerate(X.rvs(size=n)):
            realret[i] = self.rvcrapmap[h]
        return realret


class Grammar:
    """This does like everything"""
    def __init__(self):
        self.terms = set()
        self.nonterms = set()
        self.rules = {}
        self.frames = []
        # frames is a list of dicts following the templatey thingy:
        # {"var name": Data(type, stars, value)}

    def add_rule(self, nonterm: str, term: dict):
        X = ProbabilityDistribution(nonterm)
        for expansion, p in term.items():
            X[expansion] = p
        self.rules[nonterm] = X

    def add_terminals(self, terminals: set):
        assert not terminals & self.nonterms
        self.terms |= terminals

    def add_nonterminals(self, nonterminals: set):
        assert not nonterminals & self.terms
        self.nonterms |= nonterminals

    def rm_terminals(self, terminals: set):
        self.terms -= terminals

    def rm_nonterminals(self, nonterminals: set):
        self.nonterms -= nonterminals

    def expand(self, nonterm, tab=0):
        assert nonterm in self.nonterms
        ret = []
        tokens = list(self.rules[nonterm]()[0])
        for i, tok in enumerate(tokens):
            if callable(tok):
                tok = tok(self, nonterm, tokens)
                tokens[i] = tok
            if tok in self.terms:
                ret.append(tok)
            elif tok in self.nonterms:
                newtok = self.expand(tok, tab+4)
                ret.extend(newtok)
            else:
                # well looks like it's a terminal
                ret.append(tok)
        return ret

