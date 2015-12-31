if True:
    rules = {
        "S": {
            ("NP", "VP"): 1
        },
        "NP": {
            ("A", "NP"): .3,
            ("N",): .7,
        },
        "VP": {
            ("V", "NP"): .5,
            ("V",): .5,
        },
        "N": {
            ('ideas',): .5,
            ('linguists',): .5,
        },
        "V": {
            ("hate",): .5,
            ("generate",): .5,
        },
        "A": {
            ("great",): .5,
            ("green",): .5,
        }
    }

    english = Grammar()
    english.add_terminals({'generate', 'hate', 'great', 'green', 'ideas', 'linguists'})
    english.add_nonterminals({"S", 'NP', 'VP', 'N', 'V', 'A'})
    for k, v in rules.items():
        english.add_rule(k, v)

    print(english.expand("S"))
