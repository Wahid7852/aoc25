def solve_safe(rotations):
    position = 50
    count_zeros = 0
    
    for rotation in rotations:
        direction = rotation[0]
        distance = int(rotation[1:])
        
        if direction == 'L':
            position = (position - distance) % 100
        else:
            position = (position + distance) % 100
        
        if position == 0:
            count_zeros += 1
    
    return count_zeros

def count_zeros(rotations):
    position = 50
    zero_count = 0
    
    for rotation in rotations:
        direction = rotation[0]
        amount = int(rotation[1:])
        
        if direction == 'L':
            for step in range(amount):
                position = (position - 1) % 100
                if position == 0:
                    zero_count += 1
        else:  # direction == 'R'
            for step in range(amount):
                position = (position + 1) % 100
                if position == 0:
                    zero_count += 1
    
    return zero_count


with open('inputs/day1_input.txt', 'r') as f:
    rotations = [line.strip() for line in f.readlines()]
    example_rotations = f.read().strip().split()

password = solve_safe(rotations)
result = count_zeros(example_rotations)
print(f"Password: {password}")
print(f"Password: {result}")

