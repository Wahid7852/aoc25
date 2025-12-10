from itertools import combinations

def get_size(x1, y1, x2, y2):
    return (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1)

def part1(puzzle_input: str) -> int:
    corners = [tuple(map(int, line.split(','))) for line in puzzle_input.splitlines()]
    largest = 0

    for (x1, y1), (x2, y2) in combinations(corners, 2):
        area = get_size(x1, y1, x2, y2)
        if area > largest:
            largest = area
    return largest


def part2(puzzle_input: str) -> int:
    corners = [tuple(map(int, line.split(','))) for line in puzzle_input.splitlines()]
    n = len(corners)

    edges = []
    sizes = []

    for i in range(n):
        edges.append(sorted((corners[i], corners[i - 1])))

        for j in range(i + 1, n):
            c1, c2 = sorted((corners[i], corners[j]))
            size = get_size(*c1, *c2)
            sizes.append((size, c1, c2))

    edges.sort(reverse=True, key=lambda e: get_size(*e[0], *e[1]))
    sizes.sort(reverse=True)

    for size, (x1, y1), (x2, y2) in sizes:
        y1, y2 = sorted((y1, y2))

        bad = any(
            (x4 > x1 and x3 < x2 and    # horizontal
             y4 > y1 and y3 < y2)       # vertical
            for (x3, y3), (x4, y4) in edges
        )

        if not bad:
            return size

    return 0 

if __name__ == "__main__":
    with open("day9_input.txt") as f:
        puzzle = f.read().strip()

    print("Part 1:", part1(puzzle))
    print("Part 2:", part2(puzzle))