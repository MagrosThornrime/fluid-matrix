import displayio
import framebufferio
import rgbmatrix
import board
import time


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

# Access the Display
display = framebufferio.FramebufferDisplay(matrix, auto_refresh=False)

# Create a bitmap and palette
bitmap = displayio.Bitmap(display.width, display.height, 5)
palette = displayio.Palette(5)
palette[0] = 0x000000  # black
palette[1] = 0xFF0000  # red
palette[2] = 0x0000FF  # blue
palette[3] = 0x00FF00  # green
palette[4] = 0xFFFFFF  # white

# Create a TileGrid and Group
tilegrid = displayio.TileGrid(bitmap, pixel_shader=palette)
group = displayio.Group()
group.append(tilegrid)

# Assign the group to the display
display.root_group = group
# End of Setup Code

def draw_pixel(output, x, y, my_color):
    output[y * display.width + x] = my_color

def draw_row(output, row, my_color):
    for x in range(display.width):
        draw_pixel(output, x, row, my_color)

display.refresh()

# Speed control
delay = 0.05  # Adjust this value to change the speed (in seconds)

while True:
    for c in range(1, 5):
        for y in range(display.height):
            # Light up all LEDs in the row at once
            draw_row(bitmap, y, c)
            display.refresh()
            time.sleep(delay)

            # Turn off all LEDs in the row
            draw_row(bitmap, y, 0)
            display.refresh()
