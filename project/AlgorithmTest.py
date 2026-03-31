from GridParallel import GridParallel
from GridSequential import GridSequential

class ParallelTest:
    def test_1_initialization(self):
        print("Test 1: Mesh initialization")
        grid = GridParallel(100, 100)
        assert grid.rows == 100
        assert grid.cols == 100
        assert all(cell == 0 for row in grid.current for cell in row)
        print("Passed\n")

    def test_2_set_cell(self):
        print("Test 2: Installation of the cell")
        grid = GridParallel(100, 100)
        grid.set_cell(2, 2, 1)
        assert grid.current[2][2] == 1
        print("Passed\n")

    def test_3_clear(self):
        print("Test 3: Cleaning the grid")
        grid = GridParallel(100, 100)
        grid.random_init()
        grid.clear()
        assert all(cell == 0 for row in grid.current for cell in row)
        print("Passed\n")

    def test_4_neighbors(self):
        print("Test 4: Counting neighbors")
        grid = GridParallel(100, 100)
        grid.set_cell(0, 0, 1)
        grid.set_cell(0, 1, 1)
        grid.set_cell(1, 0, 1)
        grid.update()
        assert grid.current[1][1] == 1
        print("Passed\n")

    def test_5_update_birth(self):
        print("Test 5: The birth of a cell")
        grid = GridParallel(100, 100)
        grid.set_cell(0, 1, 1)
        grid.set_cell(1, 0, 1)
        grid.set_cell(1, 2, 1)
        grid.update()
        assert grid.current[1][1] == 1
        print("Passed\n")

    def test_6_update_survival(self):
        print("Test 6: Cell survival")
        grid = GridParallel(100, 100)
        grid.set_cell(1, 1, 1)
        grid.set_cell(1, 0, 1)
        grid.set_cell(1, 2, 1)
        grid.update()
        assert grid.current[1][1] == 1
        print("Passed\n")

    def test_7_update_death(self):
        print("Test 7: Cell death")
        grid = GridParallel(100, 100)
        grid.set_cell(1, 1, 1)
        grid.update()
        assert grid.current[1][1] == 0
        print("Passed\n")

    def test_8_random_init(self):
        print("Test 8: Random initialization")
        grid = GridParallel(100, 100)
        grid.random_init()
        assert all(cell in (0, 1) for row in grid.current for cell in row)
        print("Passed\n")

    def test_9_large_grid(self):
        print("Test 9: Large grid 700x700")
        grid = GridParallel(700, 700)
        grid.random_init()
        grid.update()
        assert all(cell in (0, 1) for row in grid.current for cell in row)
        print("Passed\n")

    def run_all_tests(self):
        self.test_1_initialization()
        self.test_2_set_cell()
        self.test_3_clear()
        self.test_4_neighbors()
        self.test_5_update_birth()
        self.test_6_update_survival()
        self.test_7_update_death()
        self.test_8_random_init()
        self.test_9_large_grid()

        grid = GridParallel(1, 1)
        grid.close_pool()

class SequentialTest:
    def test_1_initialization(self):
        print("Test 1: Mesh initialization")
        grid = GridSequential(100, 100)
        assert grid.rows == 100
        assert grid.cols == 100
        assert all(cell == 0 for row in grid.current for cell in row)
        print("Passed\n")

    def test_2_set_cell(self):
        print("Test 2: Installation of the cell")
        grid = GridSequential(100, 100)
        grid.set_cell(2, 2, 1)
        assert grid.current[2][2] == 1
        print("Passed\n")

    def test_3_clear(self):
        print("Test 3: Cleaning the grid")
        grid = GridSequential(100, 100)
        grid.random_init()
        grid.clear()
        assert all(cell == 0 for row in grid.current for cell in row)
        print("Passed\n")

    def test_4_neighbors(self):
        print("Test 4: Counting neighbors")
        grid = GridSequential(100, 100)
        grid.set_cell(0, 0, 1)
        grid.set_cell(0, 1, 1)
        grid.set_cell(1, 0, 1)
        count = grid.count_adjacent(1, 1)
        assert count == 3
        print("Passed\n")

    def test_5_update_birth(self):
        print("Test 5: The birth of a cell")
        grid = GridSequential(100, 100)
        grid.set_cell(0, 1, 1)
        grid.set_cell(1, 0, 1)
        grid.set_cell(1, 2, 1)

        grid.update()

        assert grid.current[1][1] == 1
        print("Passed\n")

    def test_6_update_survival(self):
        print("Test 6: Cell survival")
        grid = GridSequential(100, 100)
        grid.set_cell(1, 1, 1)
        grid.set_cell(1, 0, 1)
        grid.set_cell(1, 2, 1)

        grid.update()

        assert grid.current[1][1] == 1
        print("Passed\n")

    def test_7_update_death(self):
        print("Test 7: Cell death")
        grid = GridSequential(100, 100)
        grid.set_cell(1, 1, 1)

        grid.update()

        assert grid.current[1][1] == 0
        print("Passed\n")

    def test_8_random_init(self):
        print("Test 8: Random initialization")
        grid = GridSequential(100, 100)
        grid.random_init()

        assert all(cell in (0, 1) for row in grid.current for cell in row)
        print("Passed\n")

    def test_9_large_grid(self):
        print("Test 9: Large grid 700x700")
        grid = GridSequential(700, 700)
        grid.random_init()
        grid.update()
        assert all(cell in (0, 1) for row in grid.current for cell in row)
        print("Passed\n")

    def run_all_tests(self):
        self.test_1_initialization()
        self.test_2_set_cell()
        self.test_3_clear()
        self.test_4_neighbors()
        self.test_5_update_birth()
        self.test_6_update_survival()
        self.test_7_update_death()
        self.test_8_random_init()
        self.test_9_large_grid()

if __name__ == "__main__":
    sequential_tester = SequentialTest()
    sequential_tester.run_all_tests()
    print("---------")
    parallel_tester = ParallelTest()
    parallel_tester.run_all_tests()