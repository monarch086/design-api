import datetime as dt
import json

import requests
from flask import Flask, jsonify, request

API_TOKEN = "<token>"
RAPIDAPI_KEY = "<key>"

app = Flask(__name__)


def get_weather(location: str, endpoint: str, date: str):
    url_base_url = "https://weatherapi-com.p.rapidapi.com"
    url_location = f"q={location}"
    url_date = ""

    if date:
        url_date = f"dt={date}"

    url = f"{url_base_url}/{endpoint}?{url_location}&{url_date}"

    payload = {}
    headers = {"x-rapidapi-key": RAPIDAPI_KEY}

    response = requests.request("GET", url, headers=headers, data=payload)
    return json.loads(response.text)


class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv["message"] = self.message
        return rv


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route("/")
def home_page():
    return "<p><h2>KMA L2: Python Saas.</h2></p>"


@app.route(
    "/content/api/v1/integration/current",
    methods=["POST"],
)
def current_endpoint():
    start_dt = dt.datetime.now()
    json_data = request.get_json()
    url_endpoint = "current.json"

    if json_data.get("token") is None:
        raise InvalidUsage("token is required", status_code=400)

    token = json_data.get("token")

    if token != API_TOKEN:
        raise InvalidUsage("wrong API token", status_code=403)

    location = ""
    if json_data.get("location") is None:
        raise InvalidUsage("location is required", status_code=400)
    
    location = json_data.get("location")

    weather = get_weather(location, url_endpoint, None)

    end_dt = dt.datetime.now()

    result = {
        "event_start_datetime": start_dt.isoformat(),
        "event_finished_datetime": end_dt.isoformat(),
        "event_duration": str(end_dt - start_dt),
        "weather": weather,
    }

    return result
    
@app.route(
    "/content/api/v1/integration/history",
    methods=["POST"],
)
def history_endpoint():
    start_dt = dt.datetime.now()
    json_data = request.get_json()
    url_endpoint = "history.json"

    if json_data.get("token") is None:
        raise InvalidUsage("token is required", status_code=400)

    token = json_data.get("token")

    if token != API_TOKEN:
        raise InvalidUsage("wrong API token", status_code=403)

    if json_data.get("location") is None:
        raise InvalidUsage("location is required", status_code=400)
    
    location = json_data.get("location")

    if json_data.get("date") is None:
        raise InvalidUsage("date is required", status_code=400)
        
    date = json_data.get("date")

    weather = get_weather(location, url_endpoint, date)

    end_dt = dt.datetime.now()

    result = {
        "event_start_datetime": start_dt.isoformat(),
        "event_finished_datetime": end_dt.isoformat(),
        "event_duration": str(end_dt - start_dt),
        "weather": weather,
    }

    return result