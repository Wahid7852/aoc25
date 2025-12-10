def find_max_joltage(bank: str) -> int:
    largest: int = 0
    second: int = 0
    for i in range(len(bank)):
        v = int(bank[i])
        if v > largest and i != len(bank) - 1:
            largest = v
            second = int(bank[i + 1])
        elif v > second:
            second = v
    return largest * 10 + second

def overclock_joltage(bank: str) -> int:
    def inner(start_idx: int, remaining: int) -> int:
        largest = 0
        largest_idx = 0
        for i in range(start_idx, len(bank) - remaining + 1):
            v = int(bank[i])
            if v > largest:
                largest = v
                largest_idx = i
        if remaining > 1:
            return largest * 10**(remaining -1) + inner(largest_idx + 1, remaining - 1)
        else:
            return largest
    return inner(0, 12)

def solve_day3() -> int:
    with open('inputs/day3_input.txt', 'r') as f:
        lines = f.read().strip().split('\n')
    
    return sum(overclock_joltage(bank) for bank in lines)

if __name__ == "__main__":
    result = solve_day3()
    print(f"Total output joltage: {result}")
