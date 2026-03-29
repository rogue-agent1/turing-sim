#!/usr/bin/env python3
"""turing_sim - Turing machine simulator with tape visualization."""
import sys

class TuringMachine:
    def __init__(self, transitions, start, accept, reject, blank="_"):
        self.trans = transitions  # {(state, symbol): (new_state, write, direction)}
        self.start = start
        self.accept = accept
        self.reject = reject
        self.blank = blank
    def run(self, inp, max_steps=10000):
        tape = dict(enumerate(inp))
        head = 0
        state = self.start
        history = []
        for step in range(max_steps):
            sym = tape.get(head, self.blank)
            history.append((state, head, dict(tape)))
            if state == self.accept: return True, history
            if state == self.reject: return False, history
            key = (state, sym)
            if key not in self.trans: return False, history
            new_state, write, direction = self.trans[key]
            tape[head] = write
            head += 1 if direction == "R" else -1
            state = new_state
        return False, history  # timeout
    def tape_str(self, tape, head):
        if not tape: return f"[{self.blank}]"
        lo = min(min(tape.keys()), head)
        hi = max(max(tape.keys()), head)
        chars = []
        for i in range(lo, hi+1):
            c = tape.get(i, self.blank)
            chars.append(f"[{c}]" if i == head else c)
        return "".join(chars)

def test():
    # TM that accepts strings of form 0^n 1^n
    trans = {
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
    }
    tm = TuringMachine(trans, "q0", "qa", "qr")
    ok, hist = tm.run("0011")
    assert ok
    ok2, _ = tm.run("01")
    assert ok2
    ok3, _ = tm.run("001")
    assert not ok3
    ok4, _ = tm.run("")
    # empty should accept (q0 sees blank -> not in trans -> reject)
    # Actually q0 sees _ which isn't in trans, so rejects. That's correct for 0^n1^n where n>=1
    assert not ok4
    print("turing_sim: all tests passed")

if __name__ == "__main__":
    test() if "--test" in sys.argv else print("Usage: turing_sim.py --test")
