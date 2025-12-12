# backend/app.py
from flask import Flask, jsonify, request
from flask_cors import CORS
import nasa_timer
import nasa_apod
import nasa_insight
import llspacedevs
import nasa_neos
import datetime

app = Flask(__name__)
CORS(app)


@app.get("/health")
def health():
    return jsonify(status="ok")


@app.get("/api/countdown")
def get_countdown_api():
    # Try to fetch the next real launch from an external launch API. If that fails,
    # fall back to the existing placeholder target.
    try:
        launch = nasa_timer.fetch_next_launch()
        if launch:
            name, net = launch
            countdown_data = nasa_timer.get_countdown(name, net)
            return jsonify(countdown_data.__dict__)
    except Exception:
        # continue to fallback
        pass

    # Fallback placeholder (kept for resilience if the external API is unavailable)
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
    # include a compact 7-sol history for the frontend
    try:
        history = nasa_insight.get_last_n_sols(7)
    except Exception:
        history = []

    return jsonify(  # check back later to make sure this is correctly done
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
            "history": history,
        }
    )


@app.get("/api/llspacedevs")
def get_llspacedevs_api():
    """Return a compact summary (top countries) from the LLSpaceDevs data."""
    try:
        ad = llspacedevs.AstronautData()
        top = ad.get_top_countries(10)
        # convert (country, count, [names]) tuples into serializable dicts
        result = [{"country": t[0], "count": t[1], "names": t[2]} for t in top]
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.get("/api/llspacedevs/search")
def search_astronauts_api():
    """
    Search astronauts by country.
    """
    country = request.args.get("country")
    if not country or not country.strip():
        return jsonify({"error": "Missing 'country' query parameter"}), 400
    try:
        ad = llspacedevs.AstronautData()
        astronauts = ad.get_astronauts_by_country(country)

        # also return active/inactive breakdown like top_countries() does
        all_data = ad.get_astronauts()
        active = []
        inactive = []

        for a in all_data:
            nat = a.get("nationality", "")
            if nat and country.lower() in nat.lower():
                status = (a.get("status") or {}).get("name", "")
                if status.lower() == "active":
                    active.append(a.get("name"))
                else:
                    inactive.append(a.get("name"))

        return jsonify({
            "country": country,
            "count": len(astronauts),
            "active": active,
            "inactive": inactive,
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.get("/api/neos")
def get_neos_api():
    """Query NASA NEO feed and return compact summary.

    Query params:
      - start (YYYY-MM-DD) optional (defaults to today)
      - end   (YYYY-MM-DD) optional (defaults to start; max 7-day window)
    """
    try:
        start = request.args.get("start")
        end = request.args.get("end")

        today = datetime.date.today()
        if not start:
            start_dt = today
        else:
            start_dt = datetime.date.fromisoformat(start)

        if not end:
            end_dt = start_dt
        else:
            end_dt = datetime.date.fromisoformat(end)

        # enforce max 7-day window
        if (end_dt - start_dt).days > 6:
            end_dt = start_dt + datetime.timedelta(days=6)

        feed = nasa_neos.fetch_feed(start_dt.isoformat(), end_dt.isoformat())
        summary = nasa_neos.summarize_feed(feed)
        return jsonify(summary)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.get("/api/neo/<string:neo_id>")
def get_neo_lookup_api(neo_id: str):
    """Return details for a specific NEO id."""
    try:
        data = nasa_neos.get_neo_lookup(neo_id)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.get("/api/neo/browse")
def get_neo_browse_api():
    """Browse NEO catalog. Optional `page` query param."""
    try:
        page = int(request.args.get("page", "0"))
        data = nasa_neos.browse_neos(page=page)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
