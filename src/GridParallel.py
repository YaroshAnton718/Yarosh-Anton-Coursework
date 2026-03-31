import random
from multiprocessing import Pool, cpu_count

class GridParallel:
    def __init__(self, rows, cols, time_steps=1):
        self.rows = rows
        self.cols = cols
        self.time_steps = time_steps

        self.current = [[0 for _ in range(cols)] for _ in range(rows)]
        self.next = [[0 for _ in range(cols)] for _ in range(rows)]

        self.num_workers = max(1, cpu_count() - 1)
        self.pool = Pool(self.num_workers)

    def clear(self):
        self.current = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

    def validate(self):
        return self.rows > 0 and self.cols > 0 and self.time_steps > 0

    def random_init(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.current[i][j] = random.randint(0, 1)

    def set_cell(self, x, y, value=1):
        if 0 <= x < self.rows and 0 <= y < self.cols:
            self.current[x][y] = value

    @staticmethod
    def process_block(args):
        block, row_start, rows, cols = args

        result = []

        for i in range(1, len(block) - 1):
            row = []
            for j in range(cols):
                count = 0

                for di in (-1, 0, 1):
                    for dj in (-1, 0, 1):
                        if di == 0 and dj == 0:
                            continue

                        ni = i + di
                        nj = j + dj

                        if 0 <= nj < cols:
                            count += block[ni][nj]

                if block[i][j] == 0:
                    row.append(1 if count == 3 else 0)
                else:
                    row.append(1 if count in (2, 3) else 0)

            result.append(row)

        return row_start, result

    def update(self):
        if not self.validate():
            return

        block_size = self.rows // self.num_workers

        for _ in range(self.time_steps):

            tasks = []

            for w in range(self.num_workers):
                start = w * block_size
                end = self.rows if w == self.num_workers - 1 else (w + 1) * block_size

                top = start - 1 if start > 0 else None
                bottom = end if end < self.rows else None

                block = []

                if top is not None:
                    block.append(self.current[top])
                else:
                    block.append([0] * self.cols)

                block.extend(self.current[start:end])

                if bottom is not None:
                    block.append(self.current[bottom])
                else:
                    block.append([0] * self.cols)

                tasks.append((block, start, self.rows, self.cols))

            results = self.pool.map(GridParallel.process_block, tasks)

            for start, part in results:
                for i, row in enumerate(part):
                    self.next[start + i] = row

            self.current = [row[:] for row in self.next]

    def close_pool(self):
        self.pool.close()
        self.pool.join()