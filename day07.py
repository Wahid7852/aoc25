SPLITTER = "^"
START = "S"

def load_input(path="day7_input.txt"):
    with open(path) as f:
        return [line.rstrip("\n") for line in f]

def part1(rows):
    total = 0
    x_set = {rows[0].index(START)}

    for row in rows[1:]:
        new_set = set()
        for x in x_set:
            if row[x] != SPLITTER:
                new_set.add(x)
            else:
                new_set.add(x - 1)
                new_set.add(x + 1)
                total += 1
        x_set = new_set

    return total

def part2(rows):
    x_to_t = {rows[0].index(START): 1}

    for row in rows[1:]:
        new_map = {}
        for x, t in x_to_t.items():
            if row[x] != SPLITTER:
                new_map[x] = new_map.get(x, 0) + t
            else:
                new_map[x - 1] = new_map.get(x - 1, 0) + t
                new_map[x + 1] = new_map.get(x + 1, 0) + t
        x_to_t = new_map

    return sum(x_to_t.values())

def main():
    rows = load_input()

    p1 = part1(rows)
    p2 = part2(rows)

    print("Part 1:", p1)
    print("Part 2:", p2)


if __name__ == "__main__":
    main()
