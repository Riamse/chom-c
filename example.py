from grammar import Grammar

from fractions import Fraction

rules = {
    "$S": {
        ("$NP", "$VP"): 1
    },
    "$NP": {
        ("$A", "$NP"): Fraction(3, 10),
        ("$N",): Fraction(7, 10),
    },
    "$VP": {
        ("$V", "$NP"): Fraction(3, 4),
        ("$V",): Fraction(1, 4),
    },
    "$N": {
        ('ideas',): .5,
        ('linguists',): .5,
    },
    "$V": {
        ("hate",): .5,
        ("generate",): .5,
    },
    "$A": {
        ("great",): .5,
        ("green",): .5,
    }
}

english = Grammar()
english.add_terminals({'generate', 'hate', 'great', 'green', 'ideas', 'linguists'})
english.add_nonterminals({"$S", '$NP', '$VP', '$N', '$V', '$A'})
for k, v in rules.items():
    english.add_rule(k, v)

print(english.expand("$S"))
