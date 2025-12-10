def is_invalid_id(num):
    s = str(num)
    length = len(s)
    
    if length % 2 != 0:
        return False
    
    mid = length // 2
    return s[:mid] == s[mid:]

def find_invalid_ids_in_range(start, end):
    invalid_ids = []
    for num in range(start, end + 1):
        if is_invalid_id(num):
            invalid_ids.append(num)
    return invalid_ids

def solve(ranges_input):
    ranges = ranges_input.strip().split(',')
    total = 0
    
    for range_str in ranges:
        range_str = range_str.strip()
        start, end = map(int, range_str.split('-'))
        invalid_ids = find_invalid_ids_in_range(start, end)
        total += sum(invalid_ids)
    
    return total

def is_invalid_id(num_str):
    length = len(num_str)
    
    for pattern_len in range(1, length // 2 + 1):
        if length % pattern_len == 0:
            pattern = num_str[:pattern_len]
            repetitions = length // pattern_len
            
            if pattern * repetitions == num_str:
                return True
    
    return False

with open('inputs/day2_input.txt', 'r') as f:
    puzzle_input = f.read()
    input_str = f.read().strip()

ranges = input_str.split(',')
total = 0

for range_str in ranges:
    start, end = map(int, range_str.split('-'))
    
    for num in range(start, end + 1):
        if is_invalid_id(str(num)):
            total += num

result = solve(puzzle_input)
print(total)
print(result)
