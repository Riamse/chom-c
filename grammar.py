#!/usr/bin/python

# TODO: add Context objects for blocks and variables and stuff.

import sys
import collections
import random

sys.setrecursionlimit(2 ** 10)

class Grammar:
    """do everything"""
    def __init__(self):
        self.terms = set()
        self.nonterms = set()
        self.rules = collections.defaultdict(list)

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
        tokens = random.choice(self.rules[nonterm])
        for tok in tokens:
            if tok in self.terms:
                ret.append(tok)
            if tok in self.nonterms:
                newtok = self.expand(tok, tab+4)
                ret.extend(newtok)
        return ret

