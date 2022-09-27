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
def test_decv_cond_valuechange(initial_state, final_state, path):
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

# [ v.reg.2, .v.reg.3, v.reg.5 ]
# Test v.reg.3. V.reg.2 is used as a temporary variable
# to pick one of two code paths A / B
# each code path should be executed only once, and
# only one of each should occur.
if_cases = [
    [[0, 0, 2], [0, 0, 2], False, 'B'],
    [[0, 0, 3], [0, 0, 3], False, 'B'],
    [[0, 1, 2], [0, 0, 2], True, 'A'],
    [[0, 3, 2], [0, 2, 2], True, 'A'],
]

@pytest.mark.parametrize('initial_state,final_state,result,path', if_cases)
def test_if_decv_code_execution(initial_state, final_state, result, path):
    # This test demonstrates how 2 register PMMN can implement
    # if (decv(p)) { codeA } else { codeB }
    # by using v.reg.2 to store a flag on the failed v.reg.p test
    # which prevents the next v.reg.2 test from failing.
    # Conditional code blocks must be triggered by a Fail result.
    # REASON:
    # The prime-encoded test algorithm only follows a conditional path once on
    # failure (i.e. there is a remainder).
    # The positive case decrements cleanly and the while block is exited for the True case.
    # The True case covers the neccesary code required to decrement and test, which is
    # also covered in the False case. Only the (multiple: p - 1) False cases follow
    # different paths.

    m = ProgramMachine(2)

    # set v.reg.2, v.reg.3, and v.reg.5

    r = 2**initial_state[0] * 3**initial_state[1] * 5**initial_state[2]
    for i in range(r):
        m.inc(0)
    m.show()

    assert prime_decode(m.counters[0]) == initial_state
    path_taken = ''
    test_result = None

    # test v.reg.3, set v.reg.2 to 1 on Fail to avoid a failing test on v.reg.3 = True case
    while m.dec(0):
        if m.dec(0):
            if m.dec(0):
                pass
            else:
                # early zero, repair
                print('EARLY ZERO B')
                #path_taken = 'B'
                m.inc(0)
                while(m.dec(1)):
                    m.inc_by(0, 3)
                #while(m.dec(0)):
                #    m.inc(1)
                path_taken += 'B'
                test_result = False
                # set v.reg.2 to 1 to avoid a failed test for 'True' path
                while(m.dec(0)):
                    m.inc(1)
                    m.inc(1)
                m.inc(1)
        else:
            # early zero, repair
            print('EARLY ZERO A')
            #path_taken = 'A'
            m.show()
            print(prime_decode(m.counters[1]))
            while(m.dec(1)):
                m.inc_by(0, 3)
            path_taken += 'B'
            test_result = False
            # set v.reg.2 to 1 to avoid a failed test for 'True' path

            while(m.dec(0)):
                m.inc(1)
                m.inc(1)
            m.inc(1)

        m.inc(1)

    # Test v.reg.2 to trigger a failed test if previous v.reg test was True

    while m.dec(1):
        if m.dec(1):
            pass
        else:
            # early zero, failed test, v.reg.2 was 0, previous v.reg test was True
            path_taken += 'A'
            test_result = True
            while(m.dec(0)):  # Reset v.reg.2 to 0
                m.inc_by(1, 2)

            while(m.dec(1)):  # Swap physical registers
                m.inc(0)

        m.inc(0)

    m.show()
    assert prime_decode(m.counters[0]) == final_state
    assert test_result == result
    assert path_taken == path


while_cases = [
    [[0, 0, 2], [], '.'],
    [[0, 0, 3], [], '.'],
    [[0, 1, 2], [], 'A.'],
    [[0, 3, 2], [], 'AAA.'],
    [[0, 5, 3], [], 'AAAAA.'],
    [[0, 6, 3], [], 'AAAAAA.'],
]


@pytest.mark.parametrize('initial_state,final_state,path', while_cases)
def test_while_decv_code_execution(initial_state, final_state, path):
    # This test demonstrates how 2 register PMMN can implement
    # a single outer program loop which can be used to iterate
    # code blocks based on the value of a virtual prime encoded
    # register.

    m = ProgramMachine(2)

    # set v.reg.2, v.reg.3, and v.reg.5

    r = 2**initial_state[0] * 3**initial_state[1] * 5**initial_state[2]
    for i in range(r):
        m.inc(0)
    m.show()

    assert prime_decode(m.counters[0]) == initial_state
    path_taken = ''

    m.dec(0)
    while m.dec(0):  # keep performing the v.reg.while if data is in reg 0
        m.inc(0)
        m.inc(0)
        # test v.reg.3, set v.reg.2 to 1 on Fail to avoid a failing test on v.reg.3 = True case
        while m.dec(0):
            if m.dec(0):
                if m.dec(0):
                    pass
                else:
                    # early zero, we are done
                    print('EARLY ZERO B')
                    path_taken += '.'
                    # clear ALL data for HALT,
                    # but set v.reg.2 to 1 to avoid a failed test for 'True' path
                    while(m.dec(1)):
                        pass
                    m.inc(1)
            else:
                # early zero, we are done
                print('EARLY ZERO A')
                path_taken += '.'
                # clear ALL data for HALT,
                # but set v.reg.2 to 1 to avoid a failed test for 'True' path
                while(m.dec(1)):
                    pass
                m.inc(1)

            m.inc(1)

        # Data is in reg 1 at this point

        # Test v.reg.2 to trigger a failed test if previous v.reg test was True
        while m.dec(1):
            if m.dec(1):
                pass
            else:
                # early zero, failed test, v.reg.2 was 0, previous v.reg test was True
                path_taken += 'A'
                while(m.dec(0)):  # Reset v.reg.2 to 0
                    m.inc_by(1, 2)

                while(m.dec(1)):  # Transfer data from 1 -> 0
                    m.inc(0)
            m.inc(0)

        m.dec(0)

    m.show()
    # The only way to break out of the outer while() which contains inner while()s acting as v.reg if()s
    # is to have both physical registers zeroed.
    # One register must be 0 to break out of the last inner while (testing a v.reg), and the other
    # must be zero to break out of the main program loop, indicating a HALT condition has been reached.
    assert prime_decode(m.counters[0]) == []
    assert prime_decode(m.counters[1]) == []
    assert m.counters[0] == 0
    assert m.counters[1] == 0
    # However, we can test what path we took and the result of arbitrary terminating computations
    # will have been present encoded in one of the data registers.
    assert path_taken == path
    # Non-terminating algorithms will continue to modify the data register, and the outer loop
    # will never terminate, as expected.
    # An alternative HALT state could be to retain the final state register value and enter an infite loop
    # within the last failed test of a if(v.reg)
