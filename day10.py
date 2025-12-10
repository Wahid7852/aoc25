import itertools
import numpy as np
from dataclasses import dataclass
from scipy.optimize import milp, Bounds, LinearConstraint

@dataclass
class Machine:
    lights_count: int
    target_light_bits: int
    button_lists: list[list[int]]
    target_joltages: list[int]

    def __post_init__(self):
        self.button_masks = [
            sum(1 << idx for idx in button)
            for button in self.button_lists
        ]

    def presses_for_lights(self):
        masks = self.button_masks
        n = len(masks)

        for k in range(n + 1):
            for combo in itertools.combinations(masks, k):
                state = 0
                for mask in combo:
                    state ^= mask
                if state == self.target_light_bits:
                    return k

        raise RuntimeError("No light configuration found")

    def presses_for_joltages(self):
        L = self.lights_count
        B = len(self.button_lists)

        A = np.zeros((L, B), dtype=int)
        for j, lights in enumerate(self.button_lists):
            for i in lights:
                A[i, j] += 1

        b = np.array(self.target_joltages, dtype=int)
        c = np.ones(B)

        cons = LinearConstraint(A, b, b)
        bounds = Bounds(0, np.inf)
        integrality = np.ones(B)

        result = milp(c=c, constraints=cons, bounds=bounds, integrality=integrality)

        if not result.success:
            raise RuntimeError("ILP failed")

        x = np.round(result.x).astype(int)

        # safe
        if not np.all(A @ x == b):
            raise RuntimeError("Invalid ILP result")

        return int(x.sum())


def parse_line(line):
    diagram = line[line.index("[")+1 : line.index("]")]
    lights_count = len(diagram)
    target_bits = 0

    for i, ch in enumerate(diagram):
        if ch == "#":
            target_bits |= (1 << i)

    between = line[line.index("]")+1 : line.index("{")].strip()
    parts = [p for p in between.split() if p]

    button_lists = []
    for p in parts:
        inside = p.strip()[1:-1]
        nums = [int(x) for x in inside.split(",")] if inside else []
        button_lists.append(nums)

    jolts = line[line.index("{")+1 : line.index("}")].split(",")
    jolts = [int(x) for x in jolts]

    return Machine(lights_count, target_bits, button_lists, jolts)


def solve_part1(machines):
    return sum(m.presses_for_lights() for m in machines)

def solve_part2(machines):
    return sum(m.presses_for_joltages() for m in machines)

def main():
    import sys
    data = sys.stdin.read().strip().splitlines()
    machines = [parse_line(line) for line in data]

    print("Part 1:", solve_part1(machines))
    print("Part 2:", solve_part2(machines))

if __name__ == "__main__":
    main()