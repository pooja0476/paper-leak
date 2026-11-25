
from flask import Flask, jsonify
from flask_cors import CORS
from pathlib import Path
import pandas as pd
import json

app = Flask(__name__)
CORS(app)

ROOT = Path(__file__).resolve().parent.parent


def read_json(filename):
    path = ROOT / filename
    if not path.exists():
        return []
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []


def read_csv(filename):
    path = ROOT / filename
    if not path.exists():
        return []
    try:
        df = pd.read_csv(path).fillna("")
        return df.to_dict(orient="records")
    except (ValueError, OSError):
        return []


@app.route("/")
def home():
    return jsonify({
        "project": "Paper Leak Sentinel",
        "message": "Backend API is running",
        "status": "success"
    })


@app.route("/api/health")
def health():
    return jsonify({"status": "healthy"})


@app.route("/api/alerts")
def alerts():
    telegram_results = read_json("telegram_ocr_results.json")
    integrated_results = read_json("integrated_results.json")

    return jsonify({
        "telegram_results": telegram_results,
        "integrated_results": integrated_results,
        "telegram_alerts": read_json("telegram_ocr_alerts.json"),
        "integrated_alerts": read_json("integrated_alerts.json")
    })


@app.route("/api/centers")
def centers():
    anomaly = read_csv("member3/outputs/anomaly_results.csv")
    metrics = read_csv("member3/outputs/centre_metrics.csv")
    history = read_csv("member3/outputs/historical_comparison.csv")
    patterns = read_csv("member3/outputs/repeated_patterns.csv")

    return jsonify({
        "anomaly_results": anomaly,
        "centre_metrics": metrics,
        "historical_comparison": history,
        "repeated_patterns": patterns
    })


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
