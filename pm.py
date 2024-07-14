"""
Python Portable Minsky Machine

Implements a Python version of
https://esolangs.org/wiki/Portable_Minsky_Machine_Notation
"""

from sympy import nextprime


class ProgramMachine:
    def __init__(self, registers, initial_state=None):
        self.counters = [0] * registers
        # Hold a concept of 'state' to simulate arbitrary instruction jumps
        # as in Minsky's original description, but not present in PMMN.
        self.state = initial_state

    def inc(self, counter):
        self.counters[counter] += 1

    def dec(self, counter, state=None):
        if state and state != self.state:
            return False
        test = bool(self.counters[counter])
        if test:
            self.counters[counter] -= 1
        return test

    ## Syntactic sugar
    def inc_by(self, counter, amount):
        self.counters[counter] += amount

    def dec_by(self, counter, amount, state=None):
        if state and state != self.state:
            return False
        test = bool(self.counters[counter])
        self.counters[counter] = max(0, self.counters[counter] - amount)
        return test

    ## I/O Extenstion

    def input(self, counter):
        pass

    def output(self, counter):
        if self.dec(counter):
            print(chr(self.counters[counter]))
            self.counters[counter] = 0

    ## Helper methods, not part of the original spec:
    def show(self):
        """Shows all set registers."""
        print("<Counter Value>")
        for k, v in enumerate(self.counters):
            print(f'< {k}: {v} >')


## Prime Encoded virtual register helpers:

def prime_decode(reg: int) -> list:
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
    return gdecode(reg)


def decode_string(reg):
    return ''.join([chr(v) for v in prime_decode(reg)])


def prime_encode(vregs: list) -> int:
    """
    Encodes a list of virtual registers into
    a single prime encoded register value.
    """
    r = 1
    p = 2
    for v in vregs:
        r *= p ** v
        p = nextprime(p)
    return r
