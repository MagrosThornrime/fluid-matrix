import math
import random
from collections.abc import Iterator
from dataclasses import dataclass


@dataclass
class SandGrain:
    color: str
    velocity: float = 0


class Sand:
    DEFAULT_GRAIN_SIZE = 5
    GRAIN_ACCELERATION = 0.1
    SAND_COLORS = ["#ffae00", "#ffb619", "#ffbc2b", "#ffc240"]
    _grains: list[list[SandGrain | None]]
    _settled: list[list[int]]

    def __init__(
        self,
        width: int,
        height: int,
        grain_size: int = DEFAULT_GRAIN_SIZE,
    ) -> None:
        self._grain_size = grain_size
        self.width, self.height = self._get_grid_position(width, height)
        self._grains = [[None] * self.width for _ in range(self.height)]
        self._settled = [[0] * self.width for _ in range(self.height)]

    def add_grains(self, x: int, y: int, pen_size: int) -> None:
        for dx in range(-pen_size, pen_size, self.grain_size):
            for dy in range(-pen_size, pen_size, self.grain_size):
                if dx**2 + dy**2 < pen_size**2 and random.random() < 0.5:
                    self.add_single_grain(x + dx, y + dy)

    def add_single_grain(self, x: int, y: int) -> None:
        grid_x, grid_y = self._get_grid_position(x, y)

        if self._can_move_to(grid_x, grid_y):
            self._grains[grid_y][grid_x] = SandGrain(random.choice(self.SAND_COLORS), 1)

    def update(self) -> None:
        for y in range(self.height - 1, -1, -1):
            for x in reversed(range(self.width)) if y % 2 == 0 else range(self.width):
                if self._grains[y][x] and self._settled[y][x] < 100:
                    self._update_grain(x, y)

    def _update_grain(self, x: int, y: int) -> None:
        target_pos: tuple[int, int] | None = None
        grain: SandGrain = self._grains[y][x]  # type: ignore

        if self._can_move_to(x, y + 1):
            grain.velocity += self.GRAIN_ACCELERATION
            target_y = int(y + grain.velocity)
            if self._can_move_to(x, target_y):
                target_pos = x, target_y
            else:
                for cur_y in range(target_y, y, -1):
                    if self._can_move_to(x, cur_y):
                        target_pos = x, cur_y
                        break
        elif self._can_move_to(x + 1, y + 1):
            target_pos = x + 1, y + 1
        elif self._can_move_to(x - 1, y + 1):
            target_pos = x - 1, y + 1
        else:
            self._settled[y][x] += 1

        if target_pos:
            self._move_grain((x, y), target_pos)

    def _can_move_to(self, x: int, y: int) -> bool:
        return (
            0 <= y < self.height and 0 <= x < self.width and self._grains[y][x] is None
        )

    def _move_grain(self, pos: tuple[int, int], target_pos: tuple[int, int]) -> None:
        self._grains[target_pos[1]][target_pos[0]] = self._grains[pos[1]][pos[0]]
        self._grains[pos[1]][pos[0]] = None

    def _get_grid_position(self, x: int, y: int) -> tuple[int, int]:
        return (
            math.floor(x / self._grain_size),
            math.floor(y / self._grain_size),
        )

    def _get_real_position(self, grid_x: int, grid_y: int) -> tuple[int, int]:
        return grid_x * self._grain_size, grid_y * self._grain_size

    def reset(self) -> None:
        for x in range(self.width):
            for y in range(self.height):
                self._grains[y][x] = None
                self._settled[y][x] = 0

    @property
    def grains_list(self) -> Iterator[tuple[int, int, str]]:
        for x in range(self.width):
            for y in range(self.height):
                if grain := self._grains[y][x]:
                    yield (x, y, grain.color)

    @property
    def grain_size(self) -> int:
        return self._grain_size
