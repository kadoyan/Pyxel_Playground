import pyxel
from key_input import KeyInput
from math import cos, sin

SCREEN_WIDTH = 256
SCREEN_HEIGHT = 256
CHECKER_SIZE = 8

# Drawing checkerboard
class DrawChecker:
    def __init__(self, width:int, height:int, x:int, y:int, scale:int):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.scale = scale
    
    def draw(self):
        color = 1
        for y in range(0, self.height, self.scale):
            for x in range(0, self.width, self.scale):
                color += 1
                paint_color = color % 15 +1
                pyxel.rect(x, y, x + self.scale, y + self.scale, paint_color)

#Make wave
from collections import deque
class WaveScreen:
    def __init__(self, width:int, height:int, x:int, y:int, wave_scale:int, fill = True):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.shift_x = 0
        self.shift_y = 0
        self.wave_scale = wave_scale
        self.count = 0
        self.screen_ptr = pyxel.screen.data_ptr()
        self.screen_width = pyxel.screen.width
        self.screen_height = pyxel.screen.height
        self.fill = fill
    
    # Horizontal
    def horizontal(self):
        self.count += 1
        if KeyInput.is_pressed(KeyInput.LEFT):
            self.shift_x -= 0.2
        if KeyInput.is_pressed(KeyInput.RIGHT):
            self.shift_x += 0.2
            
        for y in range(self.y, self.y + self.height, 1):
            start = y * self.screen_width + self.x
            end = y * self.screen_width + self.width + self.x
            source = self.screen_ptr[start:end]
            #Shift data
            shift_volume = int(self.shift_x * cos((self.count + y)/self.wave_scale))
            if self.fill:
                shifted_list = deque(source)
                shifted_list.rotate(shift_volume)
            else:
                shifted_list = self.shift_list(source, shift_volume, 0)
            self.screen_ptr[start:end] = shifted_list
         
    # Vertical
    def vertical(self):
        self.count += 1
        if KeyInput.is_pressed(KeyInput.UP):
            self.shift_y -= 0.2
        if KeyInput.is_pressed(KeyInput.DOWN):
            self.shift_y += 0.2
            
        for x in range(0, self.width, 1):
            vertical_collection = []
            for y in range(0, self.height, 1):
                point = (self.y + y) * self.screen_width + self.x + x
                v_color = self.screen_ptr[point]
                vertical_collection.append(v_color)
            # Shift data
            shift_volume = int(self.shift_y * sin((self.count + x)/self.wave_scale))
            if self.fill:
                shifted_list = deque(vertical_collection)
                shifted_list.rotate(shift_volume)
            else:
                shifted_list = self.shift_list(vertical_collection, shift_volume, 0)
            for y in range(0, self.height, 1):
                point = (self.y + y) * self.screen_width + self.x + x
                self.screen_ptr[point] = shifted_list[y]
                
    def shift_list(self, lst, shift, fill_value=0):
        if shift > 0:
            # Right
            return [fill_value] * shift + lst[:-shift]
        elif shift < 0:
            # Left
            return lst[-shift:] + [fill_value] * (-shift)
        else:
            # none
            return lst
class App:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, fps=60)
        self.checker = DrawChecker(SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, CHECKER_SIZE)
        self.wave = WaveScreen(SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 8, False)
        pyxel.run(self.update, self.draw)

    def update(self):
        pass
    
    def draw(self):
        pyxel.cls(0)
        self.checker.draw()
        self.wave.vertical()
        self.wave.horizontal()
        #GRID
        for y in range(0, SCREEN_HEIGHT, CHECKER_SIZE):
            pyxel.line(0, y, SCREEN_WIDTH, y, 0)
        for x in range(0, SCREEN_WIDTH, CHECKER_SIZE):
            pyxel.line(x, 0, x, SCREEN_HEIGHT, 0)
if __name__ == "__main__":
    App()
