import os
import json
from collections import defaultdict
from datetime import datetime
import numpy as np
from statistics import median

class TeamsMetrics:
    def __init__(self, root_folder):
        self.root_folder = root_folder
        self.data = defaultdict(lambda: defaultdict(list))  # user -> date -> list of messages
        self._load_all_jsons()

    def _load_all_jsons(self):
        for filename in os.listdir(self.root_folder):
            if filename.endswith(".json"):
                with open(os.path.join(self.root_folder, filename), "r", encoding="utf-8") as f:
                    for msg in json.load(f):
                        sender = (msg.get("chat_from") or "").strip()
                        timestamp = msg.get("timestamp", "")
                        if not sender or not timestamp:
                            continue
                        try:
                            date = datetime.fromisoformat(timestamp.replace("Z", "+00:00")).date().isoformat()
                        except Exception:
                            continue
                        self.data[sender][date].append({
                            "message": msg.get("message", ""),
                            "channel": msg.get("channel", "")
                        })

    def compute_metrics(self):
        return {
            user: {
                date: np.array([
                    len(msgs),
                    round(median([len(m["message"]) for m in msgs if m["message"]]) if msgs else 0, 2),
                    round(len({m["channel"] for m in msgs if m["channel"]}), 2)
                ])
                for date, msgs in daily_msgs.items()
            }
            for user, daily_msgs in self.data.items()
        }
