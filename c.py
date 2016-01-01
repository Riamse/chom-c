#!/usr/bin/python

# this program outputs a bunch of random C code.
# TODO: add Context objects for blocks and variables and stuff.
# ^ or maybe some function calls and context is externally kept? or?

from grammar import Grammar
from fractions import Fraction

rules = {}
rules["$DOT_H"] = {}
l = ['assert.h', 'ctype.h', 'errno.h', 'fenv.h', 'float.h', 'inttypes.h', 'iso646.h', 'limits.h', 'locale.h', 'math.h', 'setjmp.h', 'signal.h', 'stdarg.h', 'stdbool.h', 'stddef.h', 'stdint.h', 'stdio.h', 'stdlib.h', 'string.h', 'tgmath.h', 'time.h', 'uchar.h', 'wchar.h', 'wctype.h']
for p in l:
    rules["$DOT_H"][(p,)] = Fraction(1, len(l))

rules["$FILE"] = {
        ("$INCLUDES", '\n', "$DECLS", '\n'): 1
}
rules["$INCLUDE"] = {
        ("#include", "<", "$DOT_H", ">"): 1,
}
rules["$INCLUDES"] = {
        ("$INCLUDE", '\n', "$INCLUDES"): .8,
        ("",): .2,
}
rules["$TYPE"] = {("int",): 1}  # XXX
rules["$VARNAME"] = {("var",): 1}  # XXX
rules["$DECL;"] = {
        ("$TYPE", ' ', "$VARNAME", ";\n"): 1,
}
rules["$DECLS"] = {
        ("$DECL;", "$DECLS"): .6,
        ("",): .4,
}

g = Grammar()
g.add_nonterminals({k for k in rules.keys()})
for right in rules.values():
    for tokens in right:
        g.add_terminals({tok for tok in tokens if tok and tok[0] != "$"})
for k, v in rules.items():
    g.add_rule(k, v)
