from __future__ import annotations
import math
import random
from collections.abc import Iterator
from dataclasses import dataclass
from enum import Enum
from typing import Any


class ElementType(Enum):
    SAND = 0
    WATER = 1
    STONE = 2


@dataclass
class Stone:
    color: str

    def update(self, _x: int, _y: int, _world) -> None:
        return None


@dataclass
class Sand:
    color: str
    velocity: float = 0
    # stepped = False

    def update(self, x: int, y: int, world: World) -> tuple[int, int] | None:
        # if self.stepped == world.stepped:
        #     return None
        #
        # self.stepped = not self.stepped

        if self._can_move_to(x, y + 1, world):
            return x, y + 1
        elif self._can_move_to(x + 1, y + 1, world):
            return x + 1, y + 1
        elif self._can_move_to(x - 1, y + 1, world):
            return x - 1, y + 1

    def _can_move_to(self, x: int, y: int, world: World) -> bool:
        if not (0 <= y < world.height and 0 <= x < world.width):
            return False

        return world.elements[y][x] is None or isinstance(world.elements[y][x], Water)


def perpendicular_vector(x: int, y: int) -> tuple[int, int]:
    if x == 0 and y == 0:
        return 0, 0
    elif x == 0:
        return y, x
    elif y == 0:
        return y, -x
    elif x > 0 and y > 0:
        return y, -x
    elif x < 0 and y > 0:
        return y, -x
    elif x < 0 and y < 0:
        return -y, x
    elif x > 0 and y < 0:
        return y, -x
    else:
        return x, y


@dataclass
class Water:
    color: str = "#00aaff"
    DISPERSION_RATE: int = 2

    def update(self, x: int, y: int, world: World) -> tuple[int, int] | None:
        target_pos = None

        dx = world.dx
        dy = world.dy

        px, py = perpendicular_vector(dx, dy)
        random_factor = random.choice([-1, 1])
        px *= random_factor
        py *= random_factor

        if self._can_move_to(x + dx, y + dy, world):
            target_pos = x + dx, y + dy
        # elif self._can_move_to(x + dx, y + 1, world):
        #     target_pos = x + dx, y + 1
        # elif self._can_move_to(x - dx, y - 1, world):
        #     target_pos = x - dx, y - 1
        elif self._can_move_to(x + px, y + py, world):
            target_pos = x + px, y + py
        elif self._can_move_to(x - px, y - py, world):
            target_pos = x - px, y - py

        # if self._can_move_to(x + 1, y + 1, world):
        #     target_pos = x + 1, y + 1
        # # elif self._can_move_to(x + dx, y + 1, world):
        # #     target_pos = x + dx, y + 1
        # # elif self._can_move_to(x - dx, y - 1, world):
        # #     target_pos = x - dx, y - 1
        # elif self._can_move_to(x - dx, y + dx, world):
        #     target_pos = x - dx, y + dx
        # elif self._can_move_to(x + dx, y - dx, world):
        #     target_pos = x + dx, y - dx

        return target_pos

    def _can_move_to(self, x: int, y: int, world: World) -> bool:
        if not (0 <= y < world.height and 0 <= x < world.width):
            return False

        return world.elements[y][x] is None


class World:
    DEFAULT_ELEMENT_SIZE = 5
    GRAVITY = 0.1
    SAND_COLORS = ["#ffae00", "#ffb619", "#ffbc2b", "#ffc240"]
    STONE_COLORS = ["#7d7d7d", "#4d4d4d", "#333333"]
    WATER_COLORS = ["#00aaff", "#0099ff", "#0088ff", "#0077ff"]
    elements: list[list[Sand | Water | None]]
    stepped = False
    dx = 0
    dy = 1

    def __init__(
        self,
        width: int,
        height: int,
        element_size: int = DEFAULT_ELEMENT_SIZE,
    ) -> None:
        self._element_size = element_size
        self.width, self.height = self._get_grid_position(width, height)
        self.elements = [[None] * self.width for _ in range(self.height)]

    def add_elements(self, x: int, y: int, pen_size: int, el_type: ElementType) -> None:
        for dx in range(-pen_size, pen_size, self.element_size):
            for dy in range(-pen_size, pen_size, self.element_size):
                if dx**2 + dy**2 < pen_size**2:
                    self.add_single_element(x + dx, y + dy, el_type)

    def add_single_element(self, x: int, y: int, el_type: ElementType) -> None:
        grid_x, grid_y = self._get_grid_position(x, y)

        if self._can_move_to(grid_x, grid_y):
            if el_type == ElementType.SAND:
                self.elements[grid_y][grid_x] = Sand(random.choice(self.SAND_COLORS))
            elif el_type == ElementType.STONE:
                self.elements[grid_y][grid_x] = Stone(random.choice(self.STONE_COLORS))
            elif el_type == ElementType.WATER:
                self.elements[grid_y][grid_x] = Water(random.choice(self.WATER_COLORS))

    def update(self) -> None:
        shuffled_x_indexes = list(range(self.width))
        random.shuffle(shuffled_x_indexes)

        shuffled_y_indexes = list(range(self.height))
        random.shuffle(shuffled_y_indexes)

        self.stepped = not self.stepped

        for y in shuffled_y_indexes:
            for x in shuffled_x_indexes:
                if self.elements[y][x]:
                    self._update_element(x, y)

    def _update_element(self, x: int, y: int) -> None:
        target_pos = self.elements[y][x].update(x, y, self)

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
