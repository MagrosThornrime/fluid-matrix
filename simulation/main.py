import pygame as pg

from Sand import Sand

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FRAMERATE = 60


def draw_sand(screen: pg.Surface, sand: Sand) -> None:
    for x, y, color in sand.grains_list:
        rect = pg.Rect(
            (x * sand.grain_size, y * sand.grain_size), (sand.grain_size,) * 2
        )
        pg.draw.rect(screen, color, rect)


def draw_pen(screen: pg.Surface, pen_size: int) -> None:
    x, y = pg.mouse.get_pos()
    pg.draw.circle(screen, "grey", (x, y), pen_size, width=2)


def handle_add_sand(sand: Sand, pen_size: int) -> None:
    mouse_pressed, _, _ = pg.mouse.get_pressed()
    if mouse_pressed:
        sand.add_grains(*pg.mouse.get_pos(), pen_size)


def main() -> None:
    # pg setup
    pg.init()
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pg.time.Clock()
    running = True
    dt = 0
    acc = 0
    pen_size = 40

    sand = Sand(SCREEN_WIDTH, SCREEN_HEIGHT)

    # main loop
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        screen.fill("white")

        while acc >= 1 / FRAMERATE:
            sand.update()
            acc -= 1 / FRAMERATE

        keys = pg.key.get_pressed()
        if keys[pg.K_r]:
            sand.reset()
        if keys[pg.K_EQUALS] and pen_size < 100:
            pen_size += 1
        if keys[pg.K_MINUS] and pen_size > 1:
            pen_size -= 1

        handle_add_sand(sand, pen_size)
        draw_sand(screen, sand)
        draw_pen(screen, pen_size)

        pg.display.flip()
        dt = clock.tick(FRAMERATE) / 1000
        acc += dt

    pg.quit()


if __name__ == "__main__":
    main()
