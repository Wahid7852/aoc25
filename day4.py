def count_accessible_rolls(grid):
    if not grid or not grid[0]:
        return 0
    
    rows = len(grid)
    cols = len(grid[0])
    accessible = set()
    
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '@':
                # Count adjacent rolls
                adjacent_count = 0
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == '@':
                        adjacent_count += 1
                
                # Accessible if fewer than 4 adjacent rolls
                if adjacent_count < 4:
                    accessible.add((r, c))
    
    return accessible


def remove_all_accessible(grid):
    total_removed = 0
    
    while True:
        accessible = count_accessible_rolls(grid)
        if not accessible:
            break
        
        # Remove all accessible rolls
        for r, c in accessible:
            grid[r][c] = '.'
        
        total_removed += len(accessible)
    
    return total_removed


# Read input and solve
with open('inputs/day4_input.txt', 'r') as f:
    grid = [list(line.strip()) for line in f.readlines()]

result = remove_all_accessible(grid)
print(f"Total rolls removed: {result}")