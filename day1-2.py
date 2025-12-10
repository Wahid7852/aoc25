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


with open('day1_input.txt', 'r') as f:
    example_rotations = f.read().strip().split()
result = count_zeros(example_rotations)
print(f"Password: {result}")