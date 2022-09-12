import pytest
from pm import ProgramMachine, prime_decode

def test_prime_decode():
    assert prime_decode(4) == [2] 
    assert prime_decode(6) == [1, 1]
    assert prime_decode(42) == [1, 1, 0, 1]
    assert prime_decode(2**5 * 5**9) == [5, 0, 9]


def view_debug(m):
    # Temporary Debugging.
    print(f'C0: {m.counters[0]}')
    print(f'C1: {m.counters[1]}')
    print(f'R0: {prime_decode(m.counters[0])}')
    print(f'R1: {prime_decode(m.counters[1])}')


def test_state_vreg_duplicate():
    # x 0 0 ->  0 x x
    m = ProgramMachine(2, 'COPY')
    x = 4
    r = 2**x
    # set v.reg.2 to x
    for i in range(r):
        m.inc(0)

    m.inc(1); m.dec(1)
    print('Start:')
    m.show()

    while m.dec(0, 'COPY'):
        print(f'OUTER LOOP: R0: {prime_decode(m.counters[0])} -- {m.counters[0]}')
        m.inc(0)
        while m.dec(0):
            if m.dec(0):
                m.inc_by(1, 15)
            else:
                print('-------Zeroed early!--------')
                m.state = 'DONE'
                view_debug(m)
                # Adjust r1 for overshoot from this point:
                while m.dec_by(1, 15):
                    m.inc(0)
                    m.inc(0)
                m.inc(0)
                while m.dec(0):
                    m.inc(1)
        else:
            print('------------')
            view_debug(m)
            # swap 0d
            while m.dec(1):
                m.inc(0)
    assert prime_decode(m.counters[0]) == [0, x, x]


def xtest_divide_by_constant():
    r = 2**13
    for i in range(r):
        inc(0)

    assert prime_decode(counters[0]) == [13]

    while counters[0]:
        dec_by(0, 4**2)
        inc(1)

    assert counters[0] == 0 
    assert prime_decode(counters[1]) == [9]
