import pygame as pg

from World import World

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 640
FRAMERATE = 60


def draw_elements(screen: pg.Surface, world: World) -> None:
    for x, y, color in world.elements_list:
        rect = pg.Rect(
            (x * world.element_size, y * world.element_size), (world.element_size,) * 2
        )
        pg.draw.rect(screen, color, rect)


def draw_pen(screen: pg.Surface, pen_size: int) -> None:
    x, y = pg.mouse.get_pos()
    pg.draw.circle(screen, "grey", (x, y), pen_size, width=2)


def handle_add_elements(sand: World, pen_size: int) -> None:
    mouse_pressed, _, _ = pg.mouse.get_pressed()
    if mouse_pressed:
        sand.add_elements(*pg.mouse.get_pos(), pen_size)


def main() -> None:
    # pg setup
    pg.init()
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pg.time.Clock()
    running = True
    dt = 0
    acc = 0
    pen_size = 40

    world = World(SCREEN_WIDTH, SCREEN_HEIGHT, 20)

    # main loop
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        screen.fill("white")

        while acc >= 1 / FRAMERATE:
            world.update()
            acc -= 1 / FRAMERATE

        keys = pg.key.get_pressed()
        if keys[pg.K_r]:
            world.reset()
        if keys[pg.K_EQUALS] and pen_size < 100:
            pen_size += 1
        if keys[pg.K_MINUS] and pen_size > 1:
            pen_size -= 1

        handle_add_elements(world, pen_size)
        draw_elements(screen, world)
        draw_pen(screen, pen_size)

        pg.display.flip()
        dt = clock.tick(FRAMERATE) / 1000
        acc += dt

    pg.quit()


if __name__ == "__main__":
    main()
