from World import World, ElementType, perpendicular_vector

SCREEN_WIDTH = 64
SCREEN_HEIGHT = 32

def draw_elements(output, world: World) -> None:
    for x, y, color in world.elements_list:
        output[y * SCREEN_WIDTH + x] = color




def main() -> None:
    # pg setup
    pg.init()
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pg.time.Clock()
    running = True
    dt = 0
    acc = 0
    pen_size = 40
    pressed = 0

    current_el_type = ElementType.SAND

    world = World(SCREEN_WIDTH, SCREEN_HEIGHT, 1)

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

        # Changing size of drawing pen
        if keys[pg.K_EQUALS] and pen_size < 100:
            pen_size += 1
        if keys[pg.K_MINUS] and pen_size > 1:
            pen_size -= 1

        # Changing element type
        if keys[pg.K_1]:
            current_el_type = ElementType.SAND
        if keys[pg.K_2]:
            current_el_type = ElementType.WATER
        if keys[pg.K_3]:
            current_el_type = ElementType.STONE
        if keys[pg.K_0]:
            if pressed == 0:
                pressed = 1
                dx, dy = world.dx, world.dy
                print(dx, dy)
                if dx == 0 and dy == 1:
                    world.dx, world.dy = 1, 1
                if dx == 1 and dy == 1:
                    world.dx, world.dy = 1, 0
                if dx == 1 and dy == 0:
                    world.dx, world.dy = 1, -1
                if dx == 1 and dy == -1:
                    world.dx, world.dy = 0, -1
                if dx == 0 and dy == -1:
                    world.dx, world.dy = -1, -1
                if dx == -1 and dy == -1:
                    world.dx, world.dy = -1, 0
                if dx == -1 and dy == 0:
                    world.dx, world.dy = -1, 1
                if dx == -1 and dy == 1:
                    world.dx, world.dy = 0, 1

        print(pressed)
        if pressed > 0:
            pressed += 1
            if pressed > 10:
                pressed = 0

        handle_add_elements(world, pen_size, current_el_type)
        draw_elements(screen, world)
        draw_pen(screen, pen_size)

        pg.display.flip()
        dt = clock.tick(FRAMERATE) / 1000
        acc += dt

    pg.quit()


if __name__ == "__main__":
    # x, y = 2, 1
    # px, py = perpendicular_vector(x, y)
    # print(x*px + y*py)
    #
    # x, y = -2, 1
    # px, py = perpendicular_vector(x, y)
    # print(x*px + y*py)
    #
    # x, y = -2, -1
    # px, py = perpendicular_vector(x, y)
    # print(x*px + y*py)
    #
    # x, y = 2, -1
    # px, py = perpendicular_vector(x, y)
    # print(x*px + y*py)

    main()
