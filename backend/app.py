# backend/app.py
from flask import Flask, jsonify
import nasa_timer

app = Flask(__name__)


@app.get("/health")
def health():
    return jsonify(status="ok")


@app.get("/api/countdown")
def get_countdown_api():
    # Example target date (replace this with a real API call later)!!
    target_dt_str = "2025-12-31T23:59:59"

    countdown_data = nasa_timer.get_countdown("New Year's Eve Test", target_dt_str)
    return jsonify(countdown_data.__dict__)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
