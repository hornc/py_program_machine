import pytest
from pm import ProgramMachine, prime_decode

def test_incv():
    m = ProgramMachine(2)

    # set v.reg.2 to 2
    r = 2**2
    for i in range(r):
        m.inc(0)
    m.show()

    assert prime_decode(m.counters[0]) == [2]
    # increase v.reg.3 by 1 without altering v.reg.2

    while m.dec(0):
        m.inc_by(1, 3)
    m.show()

    assert prime_decode(m.counters[1]) == [2, 1]


def test_incv_multiple():
    m = ProgramMachine(2)

    # set v.reg.2 to 2
    r = 2**2
    for i in range(r):
        m.inc(0)
    m.show()

    assert prime_decode(m.counters[0]) == [2]
    # increase v.reg.3 by 1 without altering v.reg.2

    while m.dec(0):
        m.inc_by(1, 5)
    m.show()

    while m.dec(1):
        m.inc_by(0, 5)
    m.show()

    while m.dec(0):
        m.inc_by(1, 11)
    m.show()

    assert prime_decode(m.counters[1]) == [2, 0, 2, 0, 1]


def test_decv_basic():
    # Test decrementing a virtual prime-encoded register in a 2 register counter machine using PMMN
    m = ProgramMachine(2)

    # set both v.reg.2 and v.reg.3 to 2.  (2*3)**2
    r = 6**2
    for i in range(r):
        m.inc(0)
    m.show()
    assert prime_decode(m.counters[0]) == [2, 2]

    # decv(3)  decrements virtual register 3
    while m.dec(0):
        m.dec(0)
        m.dec(0)
        m.inc(1)

    m.show()
    assert prime_decode(m.counters[1]) == [2, 1]



decv_cases = [
    [[3, 0, 3], [3, 0, 3], 'A'],  # Takes the A early path for v.reg 3
    [[2, 0, 7], [2, 0, 7], 'B'],  # Takes the B early path for v.reg 3
    [[2, 1, 7], [2, 0, 7], 'Default'],  # Exact division, no early exit path
]


@pytest.mark.parametrize('initial_state,final_state,path', decv_cases)
def test_decv_cond_false(initial_state, final_state, path):
    # decrement a zeroed v.reg without damaging other regsiters
    # i.e. repair the state if zeroing early.

    m = ProgramMachine(2)

    # set v.reg.2, v.reg.3, and v.reg.5

    r = 2**initial_state[0] * 3**initial_state[1] * 5**initial_state[2] 
    for i in range(r):
        m.inc(0)
    m.show()

    assert prime_decode(m.counters[0]) == initial_state
    path_taken = 'Default'

    # decv(3)  decrements virtual register 3, which when zero should leave the other registers untouched

    while m.dec(0):
        if m.dec(0):
            if m.dec(0):
                pass
            else:
                # early zero, repair
                print('EARLY ZERO B')
                path_taken = 'B'
                m.inc(0)
                while(m.dec(1)):
                    m.inc_by(0, 3)
                while(m.dec(0)):
                    m.inc(1)

        else:
            # early zero, repair
            print('EARLY ZERO A')
            path_taken = 'A'
            m.show()
            print(prime_decode(m.counters[1]))
            while(m.dec(1)):
                m.inc_by(0, 3)
            while(m.dec(0)):
                m.inc(1)

        m.inc(1)

    m.show()
    assert prime_decode(m.counters[1]) == final_state 
    assert path_taken == path



