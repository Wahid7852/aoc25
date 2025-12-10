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

with open('day1_input.txt', 'r') as f:
    rotations = [line.strip() for line in f.readlines()]

password = solve_safe(rotations)
print(f"Password: {password}")