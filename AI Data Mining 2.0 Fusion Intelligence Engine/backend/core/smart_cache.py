import os, pickle

class SmartCache:
    def __init__(self, cache_dir="data/cache/"):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)

    def save_cache(self, name, obj):
        with open(os.path.join(self.cache_dir, name), "wb") as f:
            pickle.dump(obj, f)

    def load_cache(self, name):
        path = os.path.join(self.cache_dir, name)
        if os.path.exists(path):
            with open(path, "rb") as f:
                return pickle.load(f)
        return None
