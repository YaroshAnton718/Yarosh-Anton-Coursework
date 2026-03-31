import time
import matplotlib.pyplot as plt
from GridSequential import GridSequential
from GridParallel import GridParallel
from multiprocessing import cpu_count, Pool

class SequentialPerformance:
    def __init__(self, steps=100, runs=20):
        self.steps = steps
        self.runs = runs

    def measure_time(self, rows, cols):
        grid = GridSequential(rows, cols)
        grid.random_init()

        start = time.perf_counter()

        for _ in range(self.steps):
            grid.update()

        end = time.perf_counter()

        return (end - start) / self.steps

    def measure_full_cycle(self, rows, cols):
        grid = GridSequential(rows, cols)
        grid.random_init()

        start = time.perf_counter()

        for _ in range(self.steps):
            grid.update()

            _ = [(i, j) for i in range(rows) for j in range(cols)
                 if grid.current[i][j] == 1]

        end = time.perf_counter()

        return (end - start) / self.steps

    def run_experiments(self):
        sizes = [100, 200, 300, 400, 500, 700]
        results = []

        for size in sizes:
            times = []

            print(f"Testing {size}x{size}...")

            for _ in range(self.runs):
                t = self.measure_time(size, size)
                times.append(t)

            avg_time = sum(times) / len(times)
            cells = size * size
            fps = 1 / avg_time if avg_time > 0 else 0

            results.append({
                "size": size,
                "cells": cells,
                "time": avg_time,
                "fps": fps
            })

        return results

    def stability_test(self, size=700):
        grid = GridSequential(size, size)
        grid.random_init()

        times = []

        for _ in range(self.steps):
            start = time.perf_counter()
            grid.update()
            end = time.perf_counter()
            times.append(end - start)

        return times

    def theoretical_curve(self, results):
        cells = [r["cells"] for r in results]
        base_time = results[0]["time"]

        theory = [(c / cells[0]) * base_time for c in cells]

        return theory

    def print_table(self, results):
        print(f"{'Size':>8} | {'Cells':>10} | {'Time (ms)':>12} | {'FPS':>8}")
        print("-" * 50)

        for r in results:
            print(f"{r['size']}x{r['size']:>4} | "
                  f"{r['cells']:>10} | "
                  f"{r['time'] * 1000:>12.4f} | "
                  f"{r['fps']:>8.2f}")

    def plot_main(self, results):
        cells = [r["cells"] for r in results]
        times = [r["time"] for r in results]
        fps = [r["fps"] for r in results]

        plt.figure()
        plt.plot(cells, times)
        plt.xlabel("Number of cells")
        plt.ylabel("Time (s)")
        plt.title("Execution time vs grid size")
        plt.grid()

        plt.figure()
        plt.plot(cells, fps)
        plt.xlabel("Number of cells")
        plt.ylabel("FPS")
        plt.title("FPS vs grid size")
        plt.grid()

    def plot_complexity(self, results):
        cells = [r["cells"] for r in results]
        times = [r["time"] for r in results]
        theory = self.theoretical_curve(results)

        plt.figure()
        plt.plot(cells, times, label="Experiment")
        plt.plot(cells, theory, linestyle='--', label="Theoretical")
        plt.xlabel("Number of cells")
        plt.ylabel("Time (s)")
        plt.title("Checking the complexity of the algorithm")
        plt.legend()
        plt.grid()

    def run(self):
        results = self.run_experiments()
        self.print_table(results)

        self.plot_main(results)
        self.plot_complexity(results)

        plt.show()

class PerformanceComparison:
    def __init__(self, steps=100, runs=20):
        self.steps = steps
        self.runs = runs

    def measure_seq(self, rows, cols):
        grid = GridSequential(rows, cols)
        grid.random_init()
        start = time.perf_counter()
        for _ in range(self.steps):
            grid.update()
        end = time.perf_counter()
        return (end - start) / self.steps

    def measure_par(self, rows, cols, processes=None):
        procs = processes if processes else max(1, cpu_count() - 1)
        pool = Pool(procs)
        grid = GridParallel(rows, cols)
        grid.pool = pool
        grid.random_init()
        start = time.perf_counter()
        for _ in range(self.steps):
            grid.update()
        end = time.perf_counter()
        pool.close()
        pool.join()
        return (end - start) / self.steps

    def experiment_grid_size(self, sizes=[200, 300, 400, 500, 700]):
        results = []
        for size in sizes:
            print(f"Testing {size}x{size}...")
            seq_times = [self.measure_seq(size, size) for _ in range(self.runs)]
            par_times = [self.measure_par(size, size) for _ in range(self.runs)]
            seq_avg = sum(seq_times) / len(seq_times)
            par_avg = sum(par_times) / len(par_times)
            speedup = seq_avg / par_avg if par_avg > 0 else 0
            results.append({
                "size": size,
                "seq": seq_avg,
                "par": par_avg,
                "speedup": speedup
            })

        print(f"\n{'Size':>6} | {'Seq (ms)':>10} | {'Par (ms)':>10} | {'Speedup':>8}")
        print("-" * 45)
        for r in results:
            print(f"{r['size']:>6} | "
                  f"{r['seq']*1000:>10.2f} | "
                  f"{r['par']*1000:>10.2f} | "
                  f"{r['speedup']:>8.2f}")

        sizes_plot = [r["size"] for r in results]
        seq_times = [r["seq"] for r in results]
        par_times = [r["par"] for r in results]
        speedups = [r["speedup"] for r in results]

        plt.figure()
        plt.plot(sizes_plot, seq_times, label="Sequential")
        plt.plot(sizes_plot, par_times, label="Parallel")
        plt.xlabel("Grid size (NxN)")
        plt.ylabel("Time per step (s)")
        plt.title("Execution time vs grid size")
        plt.legend()
        plt.grid()

        plt.figure()
        plt.plot(sizes_plot, speedups, marker='o')
        plt.axhline(y=1.0, color='r', linestyle='--', label='Speedup = 1')
        plt.xlabel("Grid size (NxN)")
        plt.ylabel("Speedup")
        plt.title("Parallel speedup vs grid size")
        plt.legend()
        plt.grid()

        return results

    def experiment_process_count(self, size=700):
        max_procs = cpu_count()
        results = []

        print("Measuring sequential...")
        seq_time = self.measure_seq(size, size)

        for procs in range(1, max_procs + 1):
            print(f"Testing {procs} processes...")
            par_time = self.measure_par(size, size, processes=procs)
            speedup = seq_time / par_time if par_time > 0 else 0
            results.append({
                "procs": procs,
                "par": par_time,
                "speedup": speedup
            })

        print(f"\n{'Procs':>5} | {'Par (ms)':>10} | {'Speedup':>8}")
        print("-" * 30)
        for r in results:
            print(f"{r['procs']:>5} | {r['par']*1000:>10.2f} | {r['speedup']:>8.2f}")

        procs_plot = [r["procs"] for r in results]
        par_times = [r["par"] for r in results]
        speedups = [r["speedup"] for r in results]

        plt.figure()
        plt.plot(procs_plot, par_times, marker='o')
        plt.xlabel("Number of processes")
        plt.ylabel("Time per step (s)")
        plt.title(f"Parallel time vs processes (Grid {size}x{size})")
        plt.grid()

        plt.figure()
        plt.plot(procs_plot, speedups, marker='o')
        plt.axhline(y=1.0, color='r', linestyle='--', label='Speedup = 1')
        plt.xlabel("Number of processes")
        plt.ylabel("Speedup")
        plt.title(f"Speedup vs processes (Grid {size}x{size})")
        plt.legend()
        plt.grid()

        return results

    def experiment_generations(self, size=700, generations=[10, 50, 100, 200, 500]):
        old_steps = self.steps
        results = []

        for steps in generations:
            print(f"Testing {steps} generations...")
            self.steps = steps
            seq_time = self.measure_seq(size, size)
            par_time = self.measure_par(size, size)
            speedup = seq_time / par_time if par_time > 0 else 0
            results.append({
                "gens": steps,
                "seq": seq_time,
                "par": par_time,
                "speedup": speedup
            })

        self.steps = old_steps

        print(f"\n{'Gens':>5} | {'Seq (ms)':>10} | {'Par (ms)':>10} | {'Speedup':>8}")
        print("-" * 45)
        for r in results:
            print(f"{r['gens']:>5} | "
                  f"{r['seq']*1000:>10.2f} | "
                  f"{r['par']*1000:>10.2f} | "
                  f"{r['speedup']:>8.2f}")

        gens = [r["gens"] for r in results]
        seq_times = [r["seq"] for r in results]
        par_times = [r["par"] for r in results]
        speedups = [r["speedup"] for r in results]

        plt.figure()
        plt.plot(gens, seq_times, label="Sequential")
        plt.plot(gens, par_times, label="Parallel")
        plt.xlabel("Number of generations")
        plt.ylabel("Time per step (s)")
        plt.title("Execution time vs generations")
        plt.legend()
        plt.grid()

        plt.figure()
        plt.plot(gens, speedups, marker='o')
        plt.axhline(y=1.0, color='r', linestyle='--', label='Speedup = 1')
        plt.xlabel("Number of generations")
        plt.ylabel("Speedup")
        plt.title("Speedup vs generations")
        plt.legend()
        plt.grid()

        return results

    def run_all(self):
        self.experiment_grid_size()
        self.experiment_process_count()
        self.experiment_generations()
        plt.show()

if __name__ == "__main__":
    pc = PerformanceComparison()
    pc.run_all()

    ps = SequentialPerformance()
    ps.run()