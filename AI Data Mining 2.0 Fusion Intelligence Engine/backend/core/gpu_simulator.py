import concurrent.futures, numpy as np

class GPUSimulator:
    def __init__(self, workers=4):
        self.workers = workers

    def parallel_montecarlo(self, func, dataset, iterations=1000):
        chunk = iterations // self.workers
        results = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.workers) as executor:
            futures = [executor.submit(func, dataset, chunk) for _ in range(self.workers)]
            for f in concurrent.futures.as_completed(futures):
                results.append(f.result())
        return np.mean(results), np.std(results)
