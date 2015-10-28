#!/usr/bin/python

# this program outputs a bunch of random C code.
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


if False:
    rules = {
            "S": [("NP", "VP")],
            "NP": [("A", "NP"), ("N",)],
            "VP": [("V", "NP"), ("V"),],
            "N": [['ideas'], ['linguists']],
            "V": [['generate'], ['hate']],
            "A": [['great'], ['green']]
    }

    english = Grammar()
    english.add_terminals({'generate', 'hate', 'great', 'green', 'ideas', 'linguists'})
    english.add_nonterminals({"S", 'NP', 'VP', 'N', 'V', 'A'})
    for k, v in rules.items():
        english.rules[k] = v

    print(english.expand("S"))
    sys.exit(0)

rules = {
        "$S": [["$BLOCK"], ["$EXPR;"], ["$FLOW"], ["$IFFLOW"], ["$EXPRS"], ["$S-B"]],
        "$S-B": [["$EXPR;"], ["$FLOW"], ["$IFFLOW"], ["$EXPRS"], ["$S-B", "$S-B"],],
        "$EXPR": [
            ["$VAR"],
            ["$VAR"],
            ["$VAR"],
            ["$VAR"],
            ["$FUNC"],
            ["$FUNC"],
            ["$FUNC", "$INDEX"],
            ["$LITERAL"],
            ["$LITERAL"],
            ["$LITERAL"],
            ["$LITERAL"],
            ["$LITERAL"],
            ["$EXPR", "$OP", "$EXPR"],
        ],
        "$FUNC": [
            ["$VAR", "(", "$EXPR", ", ", "$EXPR", ")"]
        ],
        "$VAR": [
            ["varname"],
            ["varname"],
            ["varname"],
            ['func(varname)'],
            ['func(varname)'],
            ['func(varname)'],
            ['$VAR', "$INDEX"],
        ],
        "$LITERAL": [
            ["false"],
            ["true"],
            ['0'],
            ['1'],
            ['"string"'],
            ["$LITERAL", "$OP", "$LITERAL"],
        ],
        "$INDEX": [
            ["[", "$LITERAL", "]"],
        ],
        "$OP": [
            ["+"],
            ["*"],
            ["%"],
            ["/"],
            ["-"],
            ["=="],
            ["!="],
            [">"],
            ["<"],
            [">="],
            ["<="],
        ],
        "$EXPRS": [
            ["$EXPR;", "$EXPRS"],
            ["$EXPR;"],
        ],
        "$EXPR;": [
            ["$EXPR", ';']
        ],
        "$DECL;": [
            ["type", ' ', "varname", "=", "$EXPR;"],
            ["type", ' ', "varname", "=", "$EXPR;"],
            ["$DECL;", "$DECL;"],
        ],
        "${BLOCK}": [
            ("{", "$DECL;", "$BLOCK", "}"),
            ("{", "$BLOCK", "}"),
        ],
        "$BLOCK": [
            ["$S-B"],
            ["$FLOW"],
            #["$EXPRS"],
            ["$EXPR;"],
            ["$EXPR;"],
        ],
        "$IFFLOW": [
            ['if', "(", "$EXPR", ")", "${BLOCK}"],
            #['if', "(", "$EXPR", ")", "$EXPR;"],
            ["$IFFLOW", "else", " ", "$IFFLOW"],
            #["$IFFLOW", "else", " ", "${BLOCK}"],
        ],
        "$FLOW": [
            ["for", "(", "$EXPR;", "$EXPR;", "$EXPR", ")", "${BLOCK}"],
            ['do', "${BLOCK}", 'while', "(", "$EXPR", ")", ';'],
            ["$IFFLOW"],
            #["$FLOW", "$FLOW"],
        ],
}

g = Grammar()
g.add_nonterminals({k for k in rules.keys()})
for right in rules.values():
    for tokens in right:
        g.add_terminals({tok for tok in tokens if tok and tok[0] != "$"})
for k, v in rules.items():
    g.rules[k] = v

s = ''
while len(s) < 30:
    s = ''.join(g.expand("$S"))
print(s)
