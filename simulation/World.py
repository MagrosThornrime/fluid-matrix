import math
import random
from collections.abc import Iterator
from dataclasses import dataclass


@dataclass
class Sand:
    color: str
    velocity: float = 0

    def update(self, x: int, y: int, world) -> None:
        target_pos = None

        if self._can_move_to(x, y + 1, world):
            target_pos = x, y + 1
        elif self._can_move_to(x + 1, y + 1, world):
            target_pos = x + 1, y + 1
        elif self._can_move_to(x - 1, y + 1, world):
            target_pos = x - 1, y + 1

        return target_pos

    def _can_move_to(self, x: int, y: int, world) -> bool:
        if not (0 <= y < world.height and 0 <= x < world.width):
            return False

        return world.elements[y][x] is None or isinstance(world.elements[y][x], Water)


@dataclass
class Water:
    color: str

    def update(self, x: int, y: int, world) -> None:
        target_pos = None

        if self._can_move_to(x, y + 1, world):
            target_pos = x, y + 1
        elif self._can_move_to(x + 1, y, world):
            target_pos = x + 1, y + 1
        elif self._can_move_to(x - 1, y, world):
            target_pos = x - 1, y + 1

        return target_pos

    def _can_move_to(self, x: int, y: int, world) -> bool:
        if not (0 <= y < world.height and 0 <= x < world.width):
            return False

        return world._grains[y][x] is None


class World:
    DEFAULT_ELEMENT_SIZE = 5
    GRAVITY = 0.1
    SAND_COLORS = ["#ffae00", "#ffb619", "#ffbc2b", "#ffc240"]
    elements: list[list[Sand | Water | None]]

    def __init__(
        self,
        width: int,
        height: int,
        element_size: int = DEFAULT_ELEMENT_SIZE,
    ) -> None:
        self._element_size = element_size
        self.width, self.height = self._get_grid_position(width, height)
        self.elements = [[None] * self.width for _ in range(self.height)]

    def add_elements(self, x: int, y: int, pen_size: int) -> None:
        for dx in range(-pen_size, pen_size, self.element_size):
            for dy in range(-pen_size, pen_size, self.element_size):
                if dx**2 + dy**2 < pen_size**2 and random.random() < 0.5:
                    self.add_single_element(x + dx, y + dy)

    def add_single_element(self, x: int, y: int) -> None:
        grid_x, grid_y = self._get_grid_position(x, y)

        if self._can_move_to(grid_x, grid_y):
            self.elements[grid_y][grid_x] = Sand(random.choice(self.SAND_COLORS), 1)

    def update(self) -> None:
        for y in range(self.height - 1, -1, -1):
            for x in reversed(range(self.width)) if y % 2 == 0 else range(self.width):
                if self.elements[y][x]:
                    self._update_element(x, y)

    def _update_element(self, x: int, y: int) -> None:
        grain = self.elements[y][x]

        target_pos = grain.update(x, y, self)

        if target_pos:
            self._move_element((x, y), target_pos)

    def _can_move_to(self, x: int, y: int) -> bool:
        return (
            0 <= y < self.height and 0 <= x < self.width and self.elements[y][x] is None
        )

    def _move_element(self, pos: tuple[int, int], target_pos: tuple[int, int]) -> None:
        tmp = self.elements[target_pos[1]][target_pos[0]]
        self.elements[target_pos[1]][target_pos[0]] = self.elements[pos[1]][pos[0]]
        self.elements[pos[1]][pos[0]] = tmp

    def _get_grid_position(self, x: int, y: int) -> tuple[int, int]:
        return (
            math.floor(x / self._element_size),
            math.floor(y / self._element_size),
        )

    def _get_real_position(self, grid_x: int, grid_y: int) -> tuple[int, int]:
        return grid_x * self._element_size, grid_y * self._element_size

    def reset(self) -> None:
        for x in range(self.width):
            for y in range(self.height):
                self.elements[y][x] = None

    @property
    def elements_list(self) -> Iterator[tuple[int, int, str]]:
        for x in range(self.width):
            for y in range(self.height):
                if element := self.elements[y][x]:
                    yield (x, y, element.color)

    @property
    def element_size(self) -> int:
        return self._element_size
