from __future__ import annotations
import math
import random

def shuffle(lst):
    for i in range(len(lst) - 1, 0, -1):
        j = random.randint(0, i)
        lst[i], lst[j] = lst[j], lst[i]

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


class Stone:
    
    def __init__(self, color: int):
        self.color = color

    def update(self, _x: int, _y: int, _world) -> None:
        return None


class Sand:    
    def __init__(self, color: int, velocity: float = 0):
        self.color = color
        self.velocity = velocity

    def update(self, x: int, y: int, world: World) -> tuple[int, int] | None:

        dx = world.dx
        dy = world.dy

        if (dx, dy) == (0, 1) or (dx, dy) == (0, -1):
            ax, bx = 1, -1
            ay, by = dy, dy
        elif (dx, dy) == (1, 0) or (dx, dy) == (-1, 0):
            ax, bx = dx, dx
            ay, by = 1, -1

        if self._can_move_to(x + dx, y + dy, world):
            return x + dx, y + dy
        elif self._can_move_to(x + ax, y + ay, world):
            return x + ax, y + ay
        elif self._can_move_to(x + bx, y + by, world):
            return x + bx, y + by

    def _can_move_to(self, x: int, y: int, world: World) -> bool:
        if not (0 <= y < world.height and 0 <= x < world.width):
            return False

        return world.elements[y][x] is None or isinstance(world.elements[y][x], Water)


class Water:
    
    def __init__(self, color: int = 8, DISPERSION_RATE: int = 2):
        self.color = color
        self.DISPERSION_RATE = DISPERSION_RATE

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
        elif self._can_move_to(x + px, y + py, world):
            target_pos = x + px, y + py
        elif self._can_move_to(x - px, y - py, world):
            target_pos = x - px, y - py

        return target_pos

    def _can_move_to(self, x: int, y: int, world: World) -> bool:
        if not (0 <= y < world.height and 0 <= x < world.width):
            return False

        return world.elements[y][x] is None


class World:
    def __init__(
        self,
        width: int,
        height: int,
        element_size: int = 5,
    ) -> None:
        self.GRAVITY = 0.1
        self.SAND_COLORS = [1, 2, 3, 4]
        self.STONE_COLORS = [5, 6, 7]
        self.WATER_COLORS = [8, 9, 10, 11]
        self.elements = []
        self.stepped = False
        self.dx = 0
        self.dy = 1
        self._element_size = element_size
        self.width, self.height = self._get_grid_position(width, height)
        self.elements = [[None] * self.width for _ in range(self.height)]

    def add_elements(self, x: int, y: int, pen_size: int, el_type: str) -> None:
        for dx in range(-pen_size, pen_size, self.element_size):
            for dy in range(-pen_size, pen_size, self.element_size):
                if dx**2 + dy**2 < pen_size**2:
                    self.add_single_element(x + dx, y + dy, el_type)

    def add_single_element(self, x: int, y: int, el_type: str) -> None:
        grid_x, grid_y = self._get_grid_position(x, y)

        if self._can_move_to(grid_x, grid_y):
            if el_type == "sand":
                self.elements[grid_y][grid_x] = Sand(random.choice(self.SAND_COLORS))
            elif el_type == "stone":
                self.elements[grid_y][grid_x] = Stone(random.choice(self.STONE_COLORS))
            elif el_type == "water":
                self.elements[grid_y][grid_x] = Water(random.choice(self.WATER_COLORS))

    def update(self) -> None:
        shuffled_x_indexes = list(range(self.width))
        shuffle(shuffled_x_indexes)

        shuffled_y_indexes = list(range(self.height))
        shuffle(shuffled_y_indexes)

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
    def elements_list(self):
        for x in range(self.width):
            for y in range(self.height):
                if element := self.elements[y][x]:
                    yield (x, y, element.color)

    @property
    def element_size(self) -> int:
        return self._element_size

