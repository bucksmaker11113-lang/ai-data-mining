import json, os
from datetime import datetime

class GrowthTracker:
    def __init__(self, path="data/reports/growth_log.json"):
        self.path = path
        os.makedirs(os.path.dirname(path), exist_ok=True)
        if not os.path.exists(path):
            json.dump([], open(path, "w"))

    def log_growth(self, accuracy, roi, bias_shift):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "accuracy": accuracy,
            "roi": roi,
            "bias_shift": bias_shift
        }
        log = json.load(open(self.path))
        log.append(entry)
        json.dump(log, open(self.path, "w"), indent=4)
        print(f"[GrowthTracker] Új növekedési pont rögzítve: acc={accuracy:.2%}, roi={roi:.2f}")

    def summarize_growth(self):
        log = json.load(open(self.path))
        if not log:
            return {"accuracy_trend": 0, "roi_trend": 0, "bias_trend": 0}
        acc = [x["accuracy"] for x in log[-5:]]
        roi = [x["roi"] for x in log[-5:]]
        bias = [x["bias_shift"] for x in log[-5:]]
        return {
            "accuracy_trend": (acc[-1] - acc[0]) if len(acc) > 1 else 0,
            "roi_trend": (roi[-1] - roi[0]) if len(roi) > 1 else 0,
            "bias_trend": (bias[-1] - bias[0]) if len(bias) > 1 else 0
        }
