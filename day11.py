from collections import Counter
from typing import Iterator

class Graph:

    def __init__(self) -> None:
        self.nodes: set[str] = set()
        self.connections: dict[str, list[str]] = dict()
    
    def add_vertex(self, vertex: str) -> None:
        if vertex in self.nodes:
            return
        self.nodes.add(vertex)
        self.connections[vertex] = []
    
    def add_connection(self, from_vertex: str, to_vertex: str) -> None:
        for v in (from_vertex, to_vertex):
            self.add_vertex(v)
        if to_vertex not in self.connections[from_vertex]:
            self.connections[from_vertex].append(to_vertex)
    
    def get_adjacent(self, vertex: str) -> list[str]:
        return [adj for adj in self.connections[vertex]]

    def traverse_paths(self, start: str, *ends: str) -> Iterator[tuple[str, int]]:
        current_front = Counter([start])
        end_vertices = set(ends)
        path_counts = {v: 0 for v in end_vertices}

        while current_front:
            next_front: Counter[str] = Counter()
            for current_vertex, path_count in current_front.items():
                if current_vertex in end_vertices:
                    path_counts[current_vertex] += path_count
                    continue
                for neighbor in self.get_adjacent(current_vertex):
                    next_front[neighbor] += path_count
            current_front = next_front
        
        yield from path_counts.items()

def build_graph(input_str: str) -> Graph:
    g = Graph()
    for line in input_str.splitlines():
        vertex, connections_str = line.split(": ")
        for connected_vertex in connections_str.split():
            g.add_connection(vertex, connected_vertex)
    return g

def calculate_paths(g: Graph, start: str, end: str, required_visits: tuple[str, ...] = ()) -> int:
    if not required_visits:
        return sum(count for _, count in g.traverse_paths(start, end))
    
    total = 0
    for visited_vertex, paths_to_here in g.traverse_paths(start, *required_visits):
        remaining_visits = tuple(v for v in required_visits if v != visited_vertex)
        further_paths = calculate_paths(g=g, start=visited_vertex, end=end, required_visits=remaining_visits)
        total += paths_to_here * further_paths
    return total

def compute_solutions(input_data: str) -> tuple[int | str, ...]:
    g = build_graph(input_data)

    part1 = calculate_paths(g=g, start="you", end="out")
    print(f"Solution to part 1: {part1}")

    part2 = calculate_paths(g=g, start="svr", end="out", required_visits=("dac", "fft"))
    print(f"Solution to part 2: {part2}")

    return part1, part2

def main() -> None:
    with open('inputs/day11_input.txt', 'r') as file:
        input_data = file.read()
    compute_solutions(input_data)

if __name__ == '__main__':
    main()