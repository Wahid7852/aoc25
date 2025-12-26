from __future__ import annotations
from dataclasses import dataclass
import functools
import numpy as np
from numpy.typing import NDArray
from operator import mul
import typing as t

grid_type: t.TypeAlias = NDArray[np.int_]

empty_cell = "."
filled_cell = "#"
cell_map = {empty_cell: 0, filled_cell: 1}
reverse_map = {v: k for k, v in cell_map.items()}

@dataclass
class Area:
    dimensions: tuple[int, int]
    item_counts: tuple[int, ...]


def process_input(input_str: str) -> tuple[list[grid_type], list[Area]]:
    sections = input_str.split("\n\n")
    shape_sections = sections[:-1]
    area_sections = sections[-1]
    
    shapes = []
    areas = []

    for idx, shape_part in enumerate(map(str.splitlines, shape_sections)):
        assert idx == int(shape_part[0].split(":")[0])
        grid = np.array([[cell_map[char] for char in row] for row in shape_part[1:]], dtype=int)
        shapes.append(grid)

    for area_line in area_sections.splitlines():
        size_part, counts_part = area_line.split(": ")
        width, height = map(int, size_part.split("x"))
        counts = tuple(map(int, counts_part.split()))
        area = Area(dimensions=(width, height), item_counts=counts)
        areas.append(area)

    return shapes, areas

def convert_grid_to_int(grid: NDArray[np.int_]) -> int:
    value = 0
    for bit in grid.ravel():
        value = (value << 1) | bit
    return value

@functools.cache
def convert_int_to_grid(num: int, dimensions: tuple[int, int]) -> NDArray[np.int_]:
    total_cells = functools.reduce(mul, dimensions, 1)
    bits = np.array([(num >> pos) & 1 for pos in range(total_cells)])
    grid = np.reshape(bits, dimensions)
    return grid

def convert_grid_to_string(grid: NDArray[np.int_]) -> str:
    rows = ["".join([reverse_map[cell] for cell in row]) for row in grid]
    return "\n".join(rows)

def get_unique_signatures(grid: NDArray) -> list[int]:
    signatures = []
    for rotations in range(4):
        rotated = np.rot90(grid, rotations)
        sig = convert_grid_to_int(rotated)
        signatures.append(sig)
        flipped_sig = convert_grid_to_int(np.fliplr(rotated))
        signatures.append(flipped_sig)
    
    return list(set(map(int, signatures)))

class ShapeFitter:
    def __init__(self, shapes: t.Iterable[grid_type]) -> None:
        self.items = tuple(shape.copy() for shape in shapes)
        self.num_items = len(self.items)
        self.item_sizes = [int(shape.sum()) for shape in self.items]
        self.item_dimensions = self.items[0].shape
        assert all(grid.shape == self.item_dimensions for grid in self.items)
        self.total_bits = functools.reduce(mul, self.item_dimensions, 1)

        self.item_signatures = [get_unique_signatures(item) for item in self.items]
        self.signature_to_item: dict[int, int] = dict()
        for item_idx, shape in enumerate(shapes):
            for sig in get_unique_signatures(shape):
                assert sig not in self.signature_to_item
                self.signature_to_item[sig] = item_idx
        
        self.symmetry_groups: list[list[int]] = [[] for _ in self.items]
        for sig, item_idx in self.signature_to_item.items():
            self.symmetry_groups[int(item_idx)].append(int(sig))
        
        self.counters = {sig: np.array([int(i == item_idx) for i in range(self.num_items)]) for sig, item_idx in self.signature_to_item.items()}
        
        max_signature = 2**self.total_bits
        self.compatible_signatures: list[list[int]] = [[] for _ in range(max_signature)]
        self.grids = []

        for sig in range(max_signature):
            self.grids.append(convert_int_to_grid(sig, dimensions=self.item_dimensions))
            compatible = sorted({s for s, _ in self.signature_to_item.items() if not (s & sig)})
            if compatible:
                self.compatible_signatures[sig] = compatible
        
        self.memo: dict[tuple[int, int], dict[tuple[int, ...], NDArray[np.int_]]] = dict()
    
    def iterate_combinations(self, initial_sig: int, current_counts: NDArray[np.int_]) -> t.Iterator[tuple[int, NDArray[np.int_]]]:
        yield initial_sig, current_counts

        compatible_sigs = self.compatible_signatures[initial_sig]
        for new_sig in compatible_sigs:
            assert (new_sig & initial_sig) == 0
            combined_sig = new_sig | initial_sig
            increment = self.counters[new_sig]
            updated_counts = current_counts + increment
            yield from self.iterate_combinations(combined_sig, updated_counts)
    
    @functools.cache
    def find_all_combinations(self, initial_sig: int) -> list[tuple[int, NDArray[np.int_]]]:
        initial_counts = np.array([0 for _ in self.items], dtype=int)
        results = []
        seen = set()
        for sig, counts in self.iterate_combinations(initial_sig=initial_sig, current_counts=initial_counts):
            key = (sig, tuple(map(int, counts)))
            if key in seen:
                continue
            seen.add(key)
            results.append((sig, counts))
        return results
    
    @functools.cache
    def shift_grid(self, grid_sig: int, right_steps: int = 0, down_steps: int = 0) -> int:
        grid = self.grids[grid_sig].copy()
        if right_steps:
            grid = np.roll(grid, shift=-right_steps, axis=1)
            grid[:, -right_steps:] = 0
        if down_steps:
            grid = np.roll(grid, shift=-down_steps, axis=0)
            grid[-down_steps:, :] = 0
        return convert_grid_to_int(grid)

    def can_fit(self, dimensions: tuple[int, int], item_counts: t.Sequence[int]) -> bool:
        if any(dim == 0 for dim in dimensions):
            return sum(item_counts) == 0
        total_area = functools.reduce(mul, dimensions)
        occupied_cells = sum(count * self.item_sizes[idx] for idx, count in enumerate(item_counts))
        return occupied_cells <= total_area

def compute_solutions(input_data: str) -> tuple[int | str, ...]:
    shapes, areas = process_input(input_data)

    fitter = ShapeFitter(shapes=shapes)
    
    fitter.find_all_combinations(initial_sig=0)

    star1 = sum(1 for area in areas if fitter.can_fit(area.dimensions, area.item_counts))
    print(f"Solution to part 1: {star1}")

    star2 = sum(sum(area.item_counts) for area in areas)
    print(f"Solution to part 2: {star2}")

    return star1, star2

def main() -> None:
    with open('inputs/day12_input.txt', 'r') as file:
        input_data = file.read()
    compute_solutions(input_data)


if __name__ == '__main__':
    main()