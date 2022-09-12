"""
Python Portable Minsky Machine

Implements a Python version of
https://esolangs.org/wiki/Portable_Minsky_Machine_Notation
"""

from sympy import nextprime

counters = {}

def inc(counter):
    counters[counter] = counters.get(counter, 0) + 1


def dec(counter):
    test = bool(counters[counter])
    counters[counter] = max(0, counters.get(counter, 0) - 1)
    return test


## Syntactic sugar
def inc_by(counter, amount):
    counters[counter] = counters.get(counter, 0) + amount 


def dec_by(counter, amount):
    test = bool(counters[counter])
    counters[counter] = max(0, counters.get(counter, 0) - amount)
    return test 


## I/O Extenstion

def input(counter):
    pass

def output(counter):
    if dec(counter):
        print(chr(counters[counter]))
        counters[counter] = 0


## Helper methods, not part of the original spec:
def show():
    """Shows all set registers."""
    print("<Counter Value>")
    for k,v in counters.items():
        print(f'< {k}: {v} >')


## Prime Encoded virtual register helpers:

def prime_decode(reg):
    """
    Decodes a single register value into a list of
    multiple prime-encoded values (a string, if used for output).
    """
    def gdecode(i, p=2):
        r = []
        while i > 1:
            v = 0
            while (i % p) == 0:
                i = i // p
                v += 1
            p = nextprime(p)
            r.append(v)
        return r

    def gascii(i, p=2):
        return ''.join([chr(v) for v in gdecode(i, p)])

    return gdecode(reg)
    #return gascii(reg)
