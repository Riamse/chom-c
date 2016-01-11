# chom-c
A simple generative grammar for C code.

You'll first want to run `mkdir header_exports`, and then `perl compute_exports.pl`. Then you can run `python -i c.py` and do things to `g` as you wish.

An instance of `Grammar` maintains context in its own attributes. If you want to expand non-terminals in parallel, you need to create another `Grammar` object. `c.py` defines a function, `new_c()` to facilitate this process.
