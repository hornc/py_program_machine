#!/usr/bin/env python3

from pm import ProgramMachine, prime_decode, prime_encode, primen


class VProgramMachine(ProgramMachine):
    # Assumes only 2 registers

    def vinc(self, vreg, reg=0):
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

    def vdec(self, vreg:int, reg:int=0) -> bool:
        """ Decrease virtual.reg of reg by 1, and act as a virtual test"""
        other = 1 - reg
        vprime = primen(vreg)
        # virtual decrement and test
        # vreg is zero if reg is not cleanly divisible by vprime
        # Fake it, (until I make it)
        if self.counters[reg] % vprime != 0:
            return False  # TODO: I can't just return a bool here, I have to set one of the registers
        else:
            self.counters[reg] /= vprime
            return True  # TODO: I can't just return a bool here, I have to set one of the registers
        #self.swap()


# This is the function we are trying to implement:
def A(m, n):  # Ackermann function (2 argument)
    if m == 0:
        return n + 1
    elif n == 0:
        return A(m-1, 1)
    return A(m-1, A(m, n-1))


# Because we can't do recursion and don't have stacks in a register machine
# this is more like the function we are trying to implement:
def ack_reg(m, n, cellwidth=10**5):
    """
    Non-recursive Ackermann function which uses a single register
    to simulate a stack (with cell width = cellwidth),
    Base algorithm taken from Rosetta code:
    https://rosettacode.org/wiki/Ackermann_function#Python:_Without_recursive_function_calls
    """
    reg = n
    reg += m * cellwidth
    once = True  # we have to run through this at least one, even if m = 0
                 # TODO: we can handle this more directly outside the while loop...
                 # refactor...
    while once or reg // cellwidth:
        once = False
        m = reg // cellwidth - (reg // cellwidth ** 2) * cellwidth
        n = reg - reg // cellwidth * cellwidth
        print(m, n, 'reg:', reg)
        reg = reg // cellwidth ** 2  # pop 2 cells
        reg *= cellwidth  # we're going to append at least one element
        if m == 0:
            reg += n + 1
        elif m == 1:
            reg += n + 2
        elif m == 2:
            reg += 2 * n + 3
        elif m == 3:
            reg += 2**(n + 3) - 3
        elif n == 0:
            reg *= cellwidth
            reg += (m-1) * cellwidth + 1
        else:
            reg *= cellwidth**2
            reg += (m-1) * cellwidth**2 + m * cellwidth + n - 1
    return reg


def main():
    m = VProgramMachine(2)

    # Set up function arguments
    #m.inc_by(0, prime_encode([0, 2, 4]))  # m = 2, n = 4
    # Check a standard Python version gives a correct answer:
    assert A(2, 4) == 11

    m.inc_by(0, prime_encode([0, 0, 4]))  # m = 2, n = 4

    m.show()
    print(prime_decode(m.counters[0]))

    # TODO: implement the parts of the algorithm using prime encoded virtual registers
    # and implement the v_ helper methods ...

    if m.vdec(1):
        # m is not 0
        m.vinc(1)  # restore 1 after the test
        if m.vdec(2): # n != 0
            # we want n to dec here, leave it alone for now
            print('return A(m-1, A(m, n-1))')
        else:  # n == 0
            print('return A(m-1, 1)')
            # return A(m-1, 1)
    else:
        # m is 0
        # return n + 1
        m.vinc(0)
        while m.vdec(2):
            m.vinc(0)

    m.show()
    print(prime_decode(m.counters[0]))


if __name__ == '__main__':
    main()
