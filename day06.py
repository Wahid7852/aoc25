import numpy as np
from pathlib import Path

def load(path):
    txt = Path(path).read_text().splitlines()
    ops = txt[-1]
    nums = txt[:-1]
    w = max(len(r) for r in nums)
    h = len(nums)
    grid = np.array([list(r.ljust(w)) for r in nums])
    ops_row = list(ops.ljust(w))
    return grid, ops_row, w, h

def get_blocks(grid, w, h):
    blocks=[]
    cur=[]
    for c in range(w):
        col = grid[:,c]
        if all(ch==' ' for ch in col):
            if cur:
                blocks.append(cur)
                cur=[]
        else:
            cur.append(c)
    if cur: blocks.append(cur)
    return blocks

def part1(path):
    grid, ops_row, w, h = load(path)
    blocks=get_blocks(grid,w,h)
    total=0
    for cols in blocks:
        # operator is under any col in block
        op='*'
        for c in cols:
            if ops_row[c]=='+': op='+'
            if ops_row[c]=='*': op='*'
        values=[]
        for r in range(h):
            s=''.join(grid[r,c] for c in cols).strip()
            if s.isdigit():
                values.append(int(s))
        if op=='+':
            total+=sum(values)
        else:
            p=1
            for v in values: p*=v
            total+=p
    return total

def part2(path):
    grid, ops_row, w, h = load(path)
    blocks=get_blocks(grid,w,h)
    total=0
    for cols in blocks:
        op='*'
        for c in cols:
            if ops_row[c]=='+': op='+'
            if ops_row[c]=='*': op='*'
        values=[]
        for c in reversed(cols):
            s=''.join(grid[r,c] for r in range(h)).strip()
            if s.isdigit():
                values.append(int(s))
        if op=='+':
            total+=sum(values)
        else:
            p=1
            for v in values: p*=v
            total+=p
    return total

if __name__=="__main__":
    path="day6_input.txt"
    print("Part1:", part1(path))
    print("Part2:", part2(path))
