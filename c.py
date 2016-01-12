#!/usr/bin/python

# this program outputs a bunch of random C code.

import random
import pickle

from grammar import Grammar
from fractions import Fraction

from common import *

def enter_scope(ctx, nonterm, tokens):
    ctx.frames.append(dict())
    ctx.tabs += 1
    return ''

def exit_scope(ctx, nonterm, tokens):
    ctx.frames.pop()
    ctx.tabs -= 1
    return ''

with open("markov.syllable.pkl", "rb") as fp:
    m = pickle.load(fp)

def makeify_new_var():
    return ''.join(m.generate())

not_allowed = {'main', 'break', 'struct', 'unsigned', 'union', 'return', 'enum', 'float', 'while', 'if', 'typedef', 'register', 'volatile', 'auto', 'double', 'for', 'sizeof', 'goto', 'default', 'long', 'extern', 'char', 'int', 'const', 'signed', 'case', 'switch', 'continue', 'void', 'static', 'do', 'else', 'short', 'restrict', 'inline', 'alignof'}
def new_var(ctx, nonterm, tokens):
    # fortunately we're allowed to 'override' upperly scoped scopes
    # so we can just check the most recently bescopen scopes for stuff
    frame = ctx.frames[-1]
    new_var_name = makeify_new_var()
    while new_var_name in frame or new_var_name in not_allowed:
        new_var_name = makeify_new_var()  # TODO: markov chains from last year
    return new_var_name

def register_new_var(ctx, nonterm, tokens):
    # aaaaaaaaaaah
    frame = ctx.frames[-1]
    datatype, varname, self = tokens
    stars = datatype.count("*")
    datatype = datatype.replace("*", '').strip()
    frame[varname] = Data(datatype, stars, None)
    return ''

def register_new_func(ctx, nonterm, tokens):
    frame = ctx.frames[-1]
    datatype, crap, varname, crap, crap, argdecl, crap, crap, crap, crap, crap, crap, crap, self = tokens
    args = argdecl.split(', ')
    if args == ['']:
        args.clear()
    for i, arg in enumerate(args):
        type_, name = arg.split(" ")
        stars = name.count("*")
        name = name.replace("*", '')
        args[i] = name, Data(type_, stars, None)
    stars = datatype.count("*")
    type_ = datatype.replace("*", '').strip()
    datatype = Data(type_, stars, None)
    frame[varname] = Callable(datatype, dict(args))
    return ''

def register_include(ctx, nonterm, tokens):
    crap, crap, dot_h, crap, crap, self = tokens
    frame = ctx.frames[0]
    for symbol in get_exports(dot_h):
        frame[symbol] = NotAllowed()
        not_allowed.add(symbol)
    return ''

def squishify_frames(ctx):
    squished = {}
    for i in range(len(ctx.frames)):
        frame = ctx.frames[-i-1]
        for k, v in frame.items():
            if k in squished:
                continue
            squished[k] = v
    return squished

def existing_var(n):
    def wrapped(ctx, nonterm, tokens):
        # we should be searching from all frames in the squishified dict
        frame = squishify_frames(ctx)
        for k, v in tuple(frame.items()):
            if not isinstance(v, Data):
                del frame[k]
        if not frame:
            # XXX if there's no variables we're fucked
            # make an Exception that tells you to abort the line entirely?
            # but such an exception can't work if you make a new context though
            # but if you make a new context the frame's going to be empty anyway
            # so in no cases should something like this even be called if we're
            # making a new frame in the same expansion, then.
            raise Abort(n)
        return random.choice(tuple(frame.keys()))  # cba to use prob dists for this
    return wrapped

def instance_of_var(ctx, nonterm, tokens):
    frame = squishify_frames(ctx)
    var = frame[tokens[0]]
    if var.stars > 0:
        return "(void*) 0"
    if var.type in {'int', 'long', 'short'}:
        return str(int(random.random() * 2 ** 30))
    elif var.type in {'double', 'float'}:
        return str(random.random() * 2 ** 30)
    elif var.type == 'char':
        return repr(bytes([random.randint(0, 127)]).decode("ascii"))
    elif var.type == 'bool':
        return "$CONDITION"
    return 'new {}()'.format(var.type)

def assign_var(ctx, nonterm, tokens):
    varname, crap, value, self = tokens
    frame = squishify_frames(ctx)
    frame[varname] = frame[varname]._replace(value=value)
    return ''

rules = {}
rules["$DOT_H"] = {}
l = ['assert.h', 'ctype.h', 'errno.h', 'fenv.h', 'float.h', 'inttypes.h', 'iso646.h', 'limits.h', 'locale.h', 'math.h', 'setjmp.h', 'signal.h', 'stdarg.h', 'stdbool.h', 'stddef.h', 'stdint.h', 'stdio.h', 'stdlib.h', 'string.h', 'tgmath.h', 'time.h', 'uchar.h', 'wchar.h', 'wctype.h']
for p in l:
    # #pragma once exists, so we don't have to care about duplicate includes
    # however we must beware, because this does not hold true for others
    rules["$DOT_H"][(p,)] = Fraction(1, len(l))

rules["$FILE"] = {
    (enter_scope, "$INCLUDES", '\n', "$DECLS",'\n',"$FUNCDECLS", '\n', "$MAINFUNC", "\n", exit_scope): 1
}
rules["$MAINFUNC"] = {
    ("int main(int argc, char *argv[])\n{\n", enter_scope, "$DECLS", "\n", "$ASSIGNS", exit_scope, "}\n"): 1
}
rules["$FUNCDECLS"] = {
    ("$FUNCDECL", "$FUNCDECLS"): Fraction(3, 10),
    ("",): Fraction(7, 10)
}
rules["$FUNCDECL"] = {
    ("$TYPE", ' ', new_var, enter_scope, "(", "$ARGDECL", ")\n{\n", "$DECLS", '\n', "$ASSIGNS", "$MORECODE", exit_scope, "}\n", register_new_func): 1
}
rules["$ARGDECL"] = {
    ("$DECL", "$MOREARGS"): .5,
    ("",): .5
}
rules["$MOREARGS"] = {
    (', ', "$DECL", "$MOREARGS"): .4,
    ("",): .6
}
rules["$IFFLOW"] = {
    ('\t', "if", ' ', "(", "$CONDITION", ")", ' ', "$FLOWSUBORDFIN"): Fraction(1, 2),
    ('\t', "if", ' ', "(", "$CONDITION", ")", ' ', "$FLOWSUBORD", 'else', ' ', "$ELIFFLOW"): Fraction(1, 2)
}
rules["$ELIFFLOW"] = {
    ('if', ' ', "(", "$CONDITION", ")", ' ', "$FLOWSUBORDFIN"): Fraction(1, 3),
    ('if', ' ', "(", "$CONDITION", ")", ' ', "$FLOWSUBORD", 'else', ' ', "$FLOWSUBORDFIN"): Fraction(1, 3),
    ('if', ' ', "(", "$CONDITION", ")", ' ', "$FLOWSUBORD", 'else', ' ', "$ELIFFLOW"): Fraction(1, 3),

}

rules["$WHILEFLOW"] = {
    ('\t', 'while', ' ', '(', "$CONDITION", ")", ' ', "$FLOWSUBORDFIN"): 1
}
rules["$FLOWSUBORD"] = {
    ("{\n", enter_scope, "$CODE", exit_scope, "\t} "): Fraction(1, 3),
    (enter_scope, '\n', '\t', "$ASSIGN;",  exit_scope, '\t'): Fraction(2, 3)
}
rules["$FLOWSUBORDFIN"] = {
    ("{\n", enter_scope, "$CODE", exit_scope, "\t}\n"): Fraction(1, 3),
    (enter_scope, '\n','\t', "$ASSIGN;", exit_scope): Fraction(2, 3)
}
rules["$CODE"] = {
    ("$DECLS", "$ASSIGNS", "$MORECODE"): 1
}
rules["$MORECODE"] = {
    ("$IFFLOW", "$MORECODE"): Fraction(1, 10),
    ("$WHILEFLOW", "$MORECODE"): Fraction(1, 10),
    ("$ASSIGNS", "$MORECODE"): Fraction(3, 5),
    ("",): Fraction(1, 5)
}
rules["$INCLUDE"] = {
    ("#include", "<", "$DOT_H", ">", '\n', register_include): 1,
}
rules["$INCLUDES"] = {
    ("$INCLUDE", "$INCLUDES"): .8,
    ("",): .2,
}
rules["$CONDITION"] = {
    ("$EXPR", ' ', "$CMP", ' ', "$EXPR"): Fraction(7, 10),
    ("$EXPR",): Fraction(3, 10)
}
cmpops = "&&", "==", "!=", ">", ">=", "<", "<="
rules["$CMP"] = {}
for cmpop in cmpops:
    rules["$CMP"][(cmpop,)] = Fraction(1, len(cmpops))
rules["$EXPR"] = {
    (existing_var(1), ' ', "$OP", ' ', existing_var(1)): Fraction(3, 10),
    (existing_var(1),): Fraction(5, 10),
    ("!", existing_var(1)): Fraction(2, 10)
}
ops = "+", '-', '/', "*", #">>", "<<", "&", "|"
rules["$OP"] = {}
for op in ops:
    rules["$OP"][(op,)] = Fraction(1, len(ops))
_types = ['int', 'char', 'long', 'short', 'float', 'double']
_types = [t + ' ' for t in _types.copy()]
types = [t.strip() + " *" for t in _types if 1==0] +  _types  # start small
rules["$TYPE"] = {}
for t in types:
    rules["$TYPE"][(t,)] = Fraction(1, len(types))
rules["$DECL"] = {
    ("$TYPE", new_var, register_new_var): 1,
}
rules["$DECL;"] = {
    ("$DECL", ";\n"): 1,
}
rules["$DECLS"] = {
    ('\t', "$DECL;", "$DECLS"): .6,
    ("",): .4,
}
rules["$ASSIGN"] = {
    (existing_var(0), ' = ', instance_of_var, assign_var): 1
}
rules["$ASSIGN;"] = {
    ("$ASSIGN", ";\n"): 1
}
rules["$ASSIGNS"] = {
    ('\t', "$ASSIGN;", "$ASSIGNS"): .6,
    ("",): .4,
}


def new_c():
    ret = Grammar()
    ret.add_nonterminals({k for k in rules.keys()})
    for right in rules.values():
        for tokens in right:
            ret.add_terminals({tok for tok in tokens if tok and (callable(tok) or (isinstance(tok, str) and tok[0] != "$"))})
    for k, v in rules.items():
        ret.add_rule(k, v)
    return ret


g = new_c()
