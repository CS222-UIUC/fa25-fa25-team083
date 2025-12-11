# backend/app.py
from flask import Flask, jsonify
from flask_cors import CORS
import nasa_timer
import nasa_apod
import nasa_insight

app = Flask(__name__)
CORS(app)


@app.get("/health")
def health():
    return jsonify(status="ok")


@app.get("/api/countdown")
def get_countdown_api():
    # Example target date (replace this with a real API call later)!!
    target_dt_str = "2025-12-31T23:59:59"

    countdown_data = nasa_timer.get_countdown("New Year's Eve Test", target_dt_str)
    return jsonify(countdown_data.__dict__)


@app.get("/api/apod")
def get_apod_api():
    apod = nasa_apod.get_APOD_lookback()
    return jsonify(apod.__dict__)


@app.get("/api/mars-insight")
def get_mars_insight_api():
    sol = nasa_insight.get_latest_sol()
    return jsonify(  # check back later to make sure this is correctlty done
        {
            "sol": sol,
            "temp": {
                "avg": nasa_insight.get_temp_avg(),
                "min": nasa_insight.get_temp_min(),
                "max": nasa_insight.get_temp_max(),
            },
            "wind": {
                "avg": nasa_insight.get_wind_avg(),
                "min": nasa_insight.get_wind_min(),
                "max": nasa_insight.get_wind_max(),
            },
            "pressure": {
                "avg": nasa_insight.get_pressure_avg(),
                "min": nasa_insight.get_pressure_min(),
                "max": nasa_insight.get_pressure_max(),
            },
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
