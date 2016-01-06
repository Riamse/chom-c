#!/usr/bin/python

# TODO: add Context objects for blocks and variables and stuff.

import sys
import random
import collections
from fractions import Fraction

from common import *

TWO_ZILLION = (2 ** 30 - 1) * 2 + 1

sys.setrecursionlimit(2 ** 10)


class ProbabilityDistribution:
    def __init__(self, name="X"):
        self.name = name
        self.crapmap = {}
        self.rvcrapmap = {}
        self.crap = []
        self.c = 0

    def __repr__(self):
        return "{.__name__}(name={!r})".format(type(self), self.name)

    def __setitem__(self, val, p):
        h = self.crapmap.get(val)
        if h is None:
            h = self.c
            self.c += 1
        self.crapmap[val] = h
        self.rvcrapmap[h] = val
        if h == len(self.crap):
            self.crap.append(p)
        elif h > len(self.crap):
            raise Exception("wtf behasherising")
        else:
            self.crap[h] = p

    def __getitem__(self, val):
        # returns P(X = val) for a rv X st X ~ self
        return self.crap[val]

    def __call__(self, n=1):
        realret = [None] * n
        for i, h in enumerate(self.sample(n)):
            realret[i] = self.rvcrapmap[h]
        return realret

    def robin_hood(self):
        # TODO: efficient-ify this
        pdf = self.crap.copy()
        n = len(pdf)
        a = Fraction(1, n)
        k = [0] * n
        v = [0] * n
        for i in range(n):
            k[i] = i
            v[i] = (i + 1) * a
        for q in range(n - 1):
            i = pdf.index(min(pdf))
            j = pdf.index(max(pdf))
            if i == j: break
            k[i] = j
            v[i] = i * a + pdf[i]
            pdf[j] = pdf[j] - (a - pdf[i])
            pdf[i] = a
        return pdf, k, v

    def sample(self, num):
        pdf, k, v = self.robin_hood()
        n = len(pdf)
        for _ in range(num):
            u = random.random()
            j = int(n * u)
            if u < v[j]:
                yield j
            else:
                yield k[j]


class Grammar:
    """This does like everything"""
    def __init__(self):
        self.terms = set()
        self.nonterms = set()
        self.rules = {}
        self.frames = []
        # frames is a list of dicts following the templatey thingy:
        # {"var name": Data(type, stars, value)}
        self.tabs = -1

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

    def expand(self, nonterm):
        assert nonterm in self.nonterms
        ret = collections.deque()
        tokens = list(self.rules[nonterm]()[0])
        for i, tok in enumerate(tokens):
            if callable(tok):
                try:
                    tok = tok(self, nonterm, tokens)
                except Abort:
                    return ['']
            tokens[i] = tok
            tabs = self.tabs
            if tok in self.nonterms:
                toks = self.expand(tok)
                #toks = [t.replace("\t", "\t" * tabs) for t in toks]
                ret.extend(toks)
                tokens[i] = ''.join(toks).replace("\t", "\t" * tabs)
                #tokens[i:i] = tok
            else:
                # well looks like it's a terminal after all
                tok = tok.replace("\t", "\t" * tabs)
                ret.append(tok)
        return ret

