import time
import pygame
from GridParallel import GridParallel
from UI import TextInput, Button, Renderer

class GameParallel:
    def __init__(self, width=1920, height=1080, cell_size=20):
        self.cell_size = cell_size
        grid_height = height - 50
        self.rows = grid_height // cell_size
        self.cols = width // cell_size

        self.grid = GridParallel(self.rows, self.cols)
        self.renderer = Renderer(width, height, cell_size)

        self.running = False
        self.generation = 0
        self.start_time = None
        self.elapsed_time = 0
        self.update_delay = 0.1
        self.last_update = time.time()

        self.buttons = [
            Button(10, height - 40, 100, 30, "Start"),
            Button(120, height - 40, 100, 30, "Clear"),
            Button(230, height - 40, 120, 30, "Random"),
            Button(360, height - 40, 140, 30, "Apply Scale")
        ]
        self.input_size = TextInput(520, height - 40, 80, 30, str(cell_size))

    def update_grid_size(self):
        grid_height = self.renderer.height - 50
        self.rows = grid_height // self.cell_size
        self.cols = self.renderer.width // self.cell_size
        self.grid = GridParallel(self.rows, self.cols)
        self.generation = 0

    def handle_mouse(self, pos):
        for btn in self.buttons:
            if btn.is_clicked(pos):
                if btn.text in ["Start", "Pause"]:
                    self.running = not self.running
                    if self.running:
                        btn.text = "Pause"
                        self.start_time = time.time()
                    else:
                        btn.text = "Start"
                        self.elapsed_time += time.time() - self.start_time
                elif btn.text == "Clear":
                    self.grid.clear()
                    self.generation = 0
                elif btn.text == "Random":
                    self.grid.random_init()
                    self.generation = 0
                elif btn.text == "Apply Scale":
                    try:
                        new_size = int(self.input_size.text)
                        if 2 <= new_size <= 100:
                            self.cell_size = new_size
                            self.renderer.cell_size = new_size
                            self.update_grid_size()
                    except:
                        pass
                return

        j = pos[0] // self.cell_size
        i = pos[1] // self.cell_size
        self.grid.set_cell(i, j, 1)

    def run(self):
        running = True
        clock = pygame.time.Clock()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    self.input_size.handle_event(event)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse(pygame.mouse.get_pos())
                    self.input_size.handle_event(event)
                if event.type == pygame.VIDEORESIZE:
                    self.renderer.resize(event.w, event.h)
                    self.update_grid_size()
                    for btn in self.buttons:
                        btn.rect.y = event.h - 40
                    self.input_size.rect.y = event.h - 40

            if self.running and time.time() - self.last_update > self.update_delay:
                self.grid.update()
                self.generation += 1
                self.last_update = time.time()

            current_time = self.elapsed_time
            if self.running:
                current_time += time.time() - self.start_time

            fps = clock.get_fps()
            self.renderer.draw(self.grid, self.buttons, [(self.input_size, "Cell Size")],
                               self.generation, current_time, fps)
            clock.tick(60)

        self.grid.close_pool()
        pygame.quit()

if __name__ == "__main__":
    game = GameParallel()
    game.run()