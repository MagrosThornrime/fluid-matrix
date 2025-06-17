import displayio
import framebufferio
import rgbmatrix
import board

class Matrix:
    def __init__(self, screen_width: int, screen_height: int):
        self.width = screen_width
        self.height = screen_height
        self.display = self.init_display()
        self.bitmap = self.init_bitmap(self.display)
        self.old_elements = []

    def init_matrix(self) -> rgbmatrix.RGBMatrix:
        displayio.release_displays()
        matrix = rgbmatrix.RGBMatrix(
                width=self.width,
                bit_depth=1,
                rgb_pins=[board.GP0, board.GP1, board.GP2, board.GP3, board.GP4, board.GP5],
                addr_pins=[board.GP6, board.GP7, board.GP8, board.GP9],
                clock_pin=board.GP11,
                latch_pin=board.GP12,
                output_enable_pin=board.GP13,
            )
        return matrix

    def init_display(self) -> framebufferio.FramebufferDisplay:
        matrix = self.init_matrix()
        display = framebufferio.FramebufferDisplay(matrix, auto_refresh=False)
        display.refresh()
        return display

    def init_bitmap(self, display: framebufferio.FramebufferDisplay) -> displayio.Bitmap:
        colors = [
            0x000000, # default color
            0xffae00, # sand color
            0xffffff, # stone color
            0x00aaff, # water color
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

    def draw_elements(self, elements: list[tuple[int, int, int]]):
        for x, y, _ in self.old_elements:
            self.bitmap[y * self.width + x] = 0
        
        for x, y, color in elements:
            self.bitmap[y * self.width + x] = color
        
        self.old_elements = elements
        self.display.refresh()
