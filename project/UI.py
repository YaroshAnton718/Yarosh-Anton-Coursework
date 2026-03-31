import pygame

class TextInput:
    def __init__(self, x, y, w, h, text=""):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.active = False

    def draw(self, screen, font, label_text=""):
        color = (200, 200, 200) if self.active else (100, 100, 100)
        pygame.draw.rect(screen, color, self.rect, 2)

        label = font.render(label_text, True, (180, 180, 180))
        screen.blit(label, (self.rect.x, self.rect.y - 18))

        txt_surface = font.render(self.text, True, (255, 255, 255))
        screen.blit(txt_surface, (self.rect.x + 5, self.rect.y + 5))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.unicode.isdigit():
                self.text += event.unicode

class Renderer:
    def __init__(self, width, height, cell_size):
        pygame.init()

        self.width = width
        self.height = height
        self.cell_size = cell_size

        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        pygame.display.set_caption("Game of Life")

        self.font = pygame.font.SysFont(None, 24)

    def resize(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)

    def draw(self, grid, buttons, inputs, generation, elapsed_time, fps):
        self.screen.fill((0, 0, 0))

        for i in range(grid.rows):
            for j in range(grid.cols):
                if hasattr(grid, "live_cells"):
                    alive = (i, j) in grid.live_cells
                else:
                    alive = grid.current[i][j] == 1

                color = (0, 255, 0) if alive else (30, 30, 30)

                rect = pygame.Rect(
                    j * self.cell_size,
                    i * self.cell_size,
                    self.cell_size,
                    self.cell_size
                )

                pygame.draw.rect(self.screen, color, rect)

        for btn in buttons:
            btn.draw(self.screen, self.font)

        for inp, label in inputs:
            inp.draw(self.screen, self.font, label)

        gen_text = self.font.render(f"Gen: {generation}", True, (255, 255, 255))
        time_text = self.font.render(f"Time: {elapsed_time:.2f}s", True, (255, 255, 255))
        fps_text = self.font.render(f"FPS: {fps:.2f}", True, (255, 255, 255))

        self.screen.blit(gen_text, (10, 10))
        self.screen.blit(time_text, (10, 30))
        self.screen.blit(fps_text, (10, 50))

        pygame.display.flip()

class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text

    def draw(self, screen, font):
        pygame.draw.rect(screen, (70, 70, 70), self.rect)
        pygame.draw.rect(screen, (200, 200, 200), self.rect, 2)

        label = font.render(self.text, True, (255, 255, 255))
        screen.blit(label, (self.rect.x + 10, self.rect.y + 5))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)