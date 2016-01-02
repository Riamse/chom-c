#!/usr/bin/python

# Adapted from an earlier project, which as of 2 January 2016 is not on Github.

import random
from collections import defaultdict, deque

START = -1
END = -2

class MarkovChain:
    def __init__(self, degrees):
        self.degrees = degrees
        self.chain = defaultdict(list)

    def extend_corpus(self, tokens):
        padding = self.degrees - 1
        tokens = ((START,) * padding) + tokens + ((END,) * padding)
        i = 0 #- self.degrees + 1
        while i < len(tokens) - self.degrees + 1:
            ngram = tuple(tokens[i:i+self.degrees])
            #print(i, ngram)
            self.chain[ngram[:-1]].append(ngram[-1])
            i += 1

    def generate(self, start=(START,)):
        if start == (START,):
            ret = []
            cur = [START] * (self.degrees - 1)
        else:
            ret = list(start)
            cur = ret.copy()
        cur = deque(cur)
        #cur = [START] * (self.degrees - 1 - 1) + list(start)
        while True:
            next_dist = self.chain[tuple(cur)]
            nex = random.choice(next_dist)
            if nex == END:
                break
            ret.append(nex)
            cur.popleft()
            cur.append(nex)
        return ret

