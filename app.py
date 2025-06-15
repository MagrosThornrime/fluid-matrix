import displayio
import framebufferio
import rgbmatrix
import board
import busio
from World import World, perpendicular_vector
import adafruit_mpu6050 as mpu6050

## sda - 14
## scl - 15

SCREEN_WIDTH = 64
SCREEN_HEIGHT = 32
FRAMERATE = 60

def dot(vector1, vector2):
    result = 0
    for num1, num2 in zip(vector1, vector2):
        result += num1 * num2
    return result

def normalize(vector):
    norm = dot(vector, vector) ** 0.5
    return [num / norm for num in vector]

def get_velocity(accel) -> tuple[int, int]:
    accel = normalize(accel)
    vectors = {
        (0, 1, 0): (0, 1),
        (0, -1, 0): (0, -1),
        (1, 0, 0): (1, 0),
        (-1, 0, 0): (-1, 0)
    }
    max_dot = float("-inf")
    max_vector = (0, 1, 0)
    for vector in vectors.keys():
        new_dot = dot(accel, vector)
        if new_dot > max_dot:
            max_dot = new_dot
            max_vector = vector
    return vectors[max_vector]


def init_matrix() -> rgbmatrix.RGBMatrix:
    displayio.release_displays()
    matrix = rgbmatrix.RGBMatrix(
            width=64,
            bit_depth=4,
            rgb_pins=[board.GP0, board.GP1, board.GP2, board.GP3, board.GP4, board.GP5],
            addr_pins=[board.GP6, board.GP7, board.GP8, board.GP9],
            clock_pin=board.GP11,
            latch_pin=board.GP12,
            output_enable_pin=board.GP13,
        )
    return matrix

def init_display(matrix: rgbmatrix.RGBMatrix) -> framebufferio.FramebufferDisplay:
    display = framebufferio.FramebufferDisplay(matrix, auto_refresh=False)
    return display

def init_bitmap(display: framebufferio.FramebufferDisplay) -> displayio.Bitmap:
    colors = [
        0x000000, # default color
        0xffae00, 0xffb619, 0xffbc2b, 0xffc240,  # sand colors
        0x7d7d7d, 0x4d4d4d, 0x333333,  # stone colors
        0x00aaff, 0x0099ff, 0x0088ff, 0x0077ff  # water colors
    ]
    bitmap = displayio.Bitmap(display.width, display.height, len(colors))
    palette = displayio.Palette(len(colors))
    for index, color in enumerate(colors):
        palette[index] = color
    tilegrid = displayio.TileGrid(bitmap, pixel_shader=palette)
    group = displayio.Group()
    group.append(tilegrid)
    display.root_group = group
    return bitmap

def init_mpu():
    i2c = busio.I2C(sda=board.GP14, scl=board.GP15)
    # Set up the MPU6050 class 
    mpu = mpu6050.MPU6050(i2c)
    return mpu

def draw_elements(output: displayio.Bitmap, world: World) -> None:
    colored = {(x, y): color for x, y, color in world.elements_list}
    for y in range(SCREEN_HEIGHT):
        for x in range(SCREEN_WIDTH):
            output[y * SCREEN_WIDTH + x] = colored.get((x,y), 0)

def main() -> None:
    dt = 0
    acc = 0

    matrix = init_matrix()
    display = init_display(matrix)
    bitmap = init_bitmap(display)
    mpu = init_mpu()

    world = World(SCREEN_WIDTH, SCREEN_HEIGHT, 1)

    display.refresh()
    world.add_elements(20, 5, 6, "water")
    
    world.add_elements(20, 30, 6, "stone")
    
    world.add_elements(40, 20, 3, "sand")

    while True:
        accel = mpu.acceleration
        dx, dy = get_velocity(accel)
        world.dx = dx
        world.dy = dy
        while acc >= 1 / FRAMERATE:
            world.update()
            acc -= 1 / FRAMERATE

        draw_elements(bitmap, world)
        display.refresh()
        dt = 0.1
        acc += dt

