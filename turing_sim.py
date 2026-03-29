#!/usr/bin/env python3
"""turing_sim: Turing machine simulator."""
import sys

class TuringMachine:
    def __init__(self, transitions, start, accept, reject, blank="_"):
        self.transitions = transitions  # {(state, symbol): (new_state, write, direction)}
        self.start = start
        self.accept = accept
        self.reject = reject
        self.blank = blank

    def run(self, input_str, max_steps=10000):
        tape = dict(enumerate(input_str))
        head = 0
        state = self.start
        for _ in range(max_steps):
            if state == self.accept: return True, tape, head
            if state == self.reject: return False, tape, head
            symbol = tape.get(head, self.blank)
            key = (state, symbol)
            if key not in self.transitions:
                return False, tape, head
            new_state, write, direction = self.transitions[key]
            tape[head] = write
            head += 1 if direction == "R" else -1
            state = new_state
        return None, tape, head  # Didn't halt

    def tape_str(self, tape):
        if not tape: return ""
        lo = min(tape)
        hi = max(tape)
        return "".join(tape.get(i, self.blank) for i in range(lo, hi + 1)).strip(self.blank)

def test():
    # TM that accepts strings of form 0^n 1^n
    tm = TuringMachine(
        transitions={
            ("q0", "0"): ("q1", "X", "R"),
            ("q0", "Y"): ("q3", "Y", "R"),
            ("q1", "0"): ("q1", "0", "R"),
            ("q1", "Y"): ("q1", "Y", "R"),
            ("q1", "1"): ("q2", "Y", "L"),
            ("q2", "Y"): ("q2", "Y", "L"),
            ("q2", "0"): ("q2", "0", "L"),
            ("q2", "X"): ("q0", "X", "R"),
            ("q3", "Y"): ("q3", "Y", "R"),
            ("q3", "_"): ("qa", "_", "R"),
        },
        start="q0", accept="qa", reject="qr"
    )
    ok, tape, _ = tm.run("01")
    assert ok
    ok, tape, _ = tm.run("0011")
    assert ok
    ok, tape, _ = tm.run("000111")
    assert ok
    ok, tape, _ = tm.run("011")
    assert not ok
    ok, tape, _ = tm.run("0")
    assert not ok
    # Simple incrementer (binary)
    tm2 = TuringMachine(
        transitions={
            ("q0", "0"): ("q0", "0", "R"),
            ("q0", "1"): ("q0", "1", "R"),
            ("q0", "_"): ("q1", "_", "L"),
            ("q1", "0"): ("qa", "1", "R"),
            ("q1", "1"): ("q1", "0", "L"),
            ("q1", "_"): ("qa", "1", "R"),
        },
        start="q0", accept="qa", reject="qr"
    )
    ok, tape, _ = tm2.run("101")
    assert ok
    assert tm2.tape_str(tape) == "110"
    print("All tests passed!")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test": test()
    else: print("Usage: turing_sim.py test")
