from matrix import Matrix
from gyroscope import Gyroscope
from world import World

SCREEN_WIDTH = 64
SCREEN_HEIGHT = 32

if __name__ == "__main__":
    matrix = Matrix(SCREEN_WIDTH, SCREEN_HEIGHT)
    gyro = Gyroscope()

    world = World(SCREEN_WIDTH, SCREEN_HEIGHT)
    
    world.add_elements(20, 5, 8, "water")
    world.add_elements(40, 6, 5, "stone")
    world.add_elements(40, 20, 3, "sand")
    world.add_elements(50, 10, 2, "sand")

    while True:
        dx, dy = gyro.get_velocity()
        world.update(dx, dy)
        elements = [(x, y, color) for x, y, color in world.elements_list]
        matrix.draw_elements(elements)
