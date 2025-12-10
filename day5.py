import pandas as pd

def part1():
    with open('inputs/day5_input.txt') as f:
        data = f.read().strip().splitlines()

    ranges=[]
    ids=[]
    reading_ids=False
    for line in data:
        if line.strip()=="":
            reading_ids=True
            continue
        if not reading_ids:
            a,b=line.split('-')
            ranges.append((int(a),int(b)))
        else:
            ids.append(int(line.strip()))

    fresh=0
    for x in ids:
        for a,b in ranges:
            if a<=x<=b:
                fresh+=1
                break
    print(fresh)
        
def part2():
    with open("inputs/day5_input.txt") as f:
        data = f.read().strip().splitlines()

    ranges = []
    for line in data:
        if line.strip() == "":
            break
        a, b = line.split('-')
        ranges.append((int(a), int(b)))

    ranges.sort()

    merged = []
    for a, b in ranges:
        if not merged or a > merged[-1][1]:
            merged.append([a, b])
        else:
            merged[-1][1] = max(merged[-1][1], b)

    total = sum(b - a + 1 for a, b in merged)

    print(total)
