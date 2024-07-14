#!/usr/bin/env python3

from pm import ProgramMachine, prime_decode, prime_encode, primen


class VProgramMachine(ProgramMachine):
    # Assumes only 2 registers

    def vinc(self, vreg, reg):
        """ Increase virtual.reg of reg by 1."""
        other = 1 - reg
        vprime = primen(vreg)
        while self.dec(reg):
            self.inc_by(other, vprime)
        self.swap()

    def swap(self):
        # Swap regs 0 and 1
        t = self.counters[0]
        self.counters[0] = self.counters[1]
        self.counters[1] = t


    def vdec(self, vreg, reg):
        """ Decrease virtual.reg of reg by 1, and act as a virtual test"""


# This is the function we are trying to implement:
def A(m, n):  # Ackermann function (2 argument)
    if m == 0:
        return n + 1
    elif n == 0:
        return A(m-1, 1)
    return A(m-1, A(m, n-1))


def main():
    m = VProgramMachine(2)

    # Set up function arguments
    m.inc_by(0, prime_encode([0, 2, 4]))
    # Check a standard Python version gives a correct answer:
    assert A(2, 4) == 11

    m.show()
    print(prime_decode(m.counters[0]))

    # TODO: implement the parts of the algorithm using prime encoded virtual registers
    # and implement the v_ helper methods ...

    m.vinc(0, 0)
    m.show()
    print(prime_decode(m.counters[0]))


if __name__ == '__main__':
    main()
