import json, os
from datetime import datetime

class FeedbackLoop:
    def __init__(self):
        self.feedback_file = "data/feedback_log.json"
        if not os.path.exists(self.feedback_file):
            json.dump([], open(self.feedback_file, "w"))

    def record_feedback(self, system, accuracy, roi):
        """Tippmester/MZ/X visszajelzés rögzítése"""
        log = json.load(open(self.feedback_file))
        entry = {
            "timestamp": datetime.now().isoformat(),
            "system": system,
            "accuracy": accuracy,
            "roi": roi
        }
        log.append(entry)
        json.dump(log, open(self.feedback_file, "w"), indent=4)
        print(f"[Feedback] {system}: accuracy={accuracy:.2f}, roi={roi:.2f}")

    def get_average_feedback(self):
        log = json.load(open(self.feedback_file))
        if not log: return {"avg_accuracy": 0, "avg_roi": 0}
        acc = [x["accuracy"] for x in log]
        roi = [x["roi"] for x in log]
        return {"avg_accuracy": sum(acc)/len(acc), "avg_roi": sum(roi)/len(roi)}
