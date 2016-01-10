#!/usr/bin/python

import pickle
from pathlib import Path
from collections import namedtuple

__all__ = ("Data", "Callable", 'NotAllowed', "Abort", 'get_exports')

Data = namedtuple("Data", 'type stars value')
Callable = namedtuple("Callable", 'retval args')

class NotAllowed: pass

class Abort(Exception): pass

def get_exports(dot_h):
    dot_h += '.pkl'
    ret = set()
    with (Path("header_exports")/dot_h).open("rb") as fp:
        ret = pickle.load(fp)
    return ret
