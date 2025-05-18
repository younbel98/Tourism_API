import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


def load_json(name):
    with open(os.path.join(DATA_DIR, name), encoding="utf-8") as f:
        return json.load(f)


ECO_INSIGHTS = load_json("ecological_insights_per_site.json")
QUIZZES = load_json("quizzes.json")
BADGES = load_json("badges.json")
RISK_ALERTS = load_json("risk_alerts.json")
