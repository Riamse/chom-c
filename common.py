#!/usr/bin/python

from collections import namedtuple

__all__ = ("Data", "Abort")

Data = namedtuple("Data", 'type stars value')

class Abort(Exception): pass
