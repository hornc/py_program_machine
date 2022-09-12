import pytest
from pm import counters, prime_decode, inc, inc_by, dec, dec_by, show


def test_prime_decode():
    assert prime_decode(4) == [2] 
    assert prime_decode(6) == [1, 1]
    assert prime_decode(42) == [1, 1, 0, 1]
    assert prime_decode(2**5 * 5**9) == [5, 0, 9]


def test_state_vreg_copy():
    global counters
    # or duplicate  x 0 0 ->  0 x x
    x = 4
    r = 2**x
    # set v.reg.2 to x
    for i in range(r):
        inc(0)

    inc(1); dec(1) 
    print('Start:')
    show()
    state = 'COPY'

    while state == 'COPY' and dec(0):  # !! needs to be while v.reg.2 ... this currently does not know when to stop
        print(f'OUTER LOOP: R0: {prime_decode(counters[0])} -- {counters[0]}')
        inc(0)
        while dec(0):
            if dec(0):
                inc_by(1, 15)

            else:
                print('-------Zeroed early!--------')
                state = 'DONE'
                print(f'C0: {counters[0]}')
                print(f'C1: {counters[1]}')
                print(f'R0: {prime_decode(counters[0])}')
                print(f'R1: {prime_decode(counters[1])}')
                # Adjust r1 for overshoot from this point:
                #counters[1] = counters[1] // 15 * 2
                while dec_by(1, 15):
                    inc(0)
                    inc(0)
                inc(0)
                while dec(0):
                    inc(1)

        else:
            print("------------")
            print(f'C0: {counters[0]}')
            print(f'C1: {counters[1]}')
            print(f'R0: {prime_decode(counters[0])}')
            print(f'R1: {prime_decode(counters[1])}')
            # swap 0d
            while dec(1):
                inc(0)
            #counters[0] = counters[1]
            #counters[1] = 0

    
    #counters[0] = counters[0] * 2 + 15  # for [0, x+1, x+1]
    assert prime_decode(counters[0]) == [0, x, x]


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
