#!/usr/bin/python

from collections import namedtuple

__all__ = ("Data", "Callable", "Abort")

Data = namedtuple("Data", 'type stars value')
Callable = namedtuple("Callable", 'retval args')

class Abort(Exception): pass
