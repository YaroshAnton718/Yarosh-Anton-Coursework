import random

class GridSequential:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.current = [[0 for _ in range(cols)] for _ in range(rows)]
        self.next = [[0 for _ in range(cols)] for _ in range(rows)]

    def clear(self):
        self.current = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

    def random_init(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.current[i][j] = random.randint(0, 1)

    def set_cell(self, x, y, value=1):
        if 0 <= x < self.rows and 0 <= y < self.cols:
            self.current[x][y] = value

    def count_adjacent(self, x, y):
        count = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue

                nx, ny = x + i, y + j

                if 0 <= nx < self.rows and 0 <= ny < self.cols:
                    count += self.current[nx][ny]

        return count

    def update(self):
        for i in range(self.rows):
            for j in range(self.cols):
                adjacent = self.count_adjacent(i, j)

                if self.current[i][j] == 0:
                    self.next[i][j] = 1 if adjacent == 3 else 0
                else:
                    self.next[i][j] = 1 if adjacent in (2, 3) else 0

        self.current = [row[:] for row in self.next]
