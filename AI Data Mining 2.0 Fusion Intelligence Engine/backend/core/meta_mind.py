import json
from datetime import datetime

class MetaMind:
    def __init__(self):
        self.logs = []
        self.weights = {"montecarlo": 0.4, "bayes": 0.3, "reinforcement": 0.3}

    def analyze_performance(self, stats):
        accuracy = stats.get("last_accuracy", 0)
        if accuracy < 0.7:
            self.adjust_weights("bayes", +0.05)
        elif accuracy > 0.9:
            self.adjust_weights("reinforcement", +0.05)
        self.logs.append({"timestamp": datetime.now().isoformat(), "accuracy": accuracy, "weights": self.weights.copy()})

    def adjust_weights(self, key, delta):
        for k in self.weights.keys():
            if k == key:
                self.weights[k] = min(1.0, self.weights[k] + delta)
            else:
                self.weights[k] = max(0.0, self.weights[k] - delta/2)
        s = sum(self.weights.values())
        self.weights = {k: v/s for k, v in self.weights.items()}

    def export_log(self):
        with open("data/reports/meta_log.json", "w") as f:
            json.dump(self.logs, f, indent=4)
