from flask import render_template
from ..model import Event
from . import main
from datetime import datetime, date


@main.route("/", methods=["GET"])
def index():
    events = Event.query.all()
    return render_template("index.html", data=events)


@main.route("/service/<service_name>", methods=["GET"])
def services(service_name):
    if service_name.lower() == "berghain":
        events = Event.query.filter_by(source_id=1).all()
    elif service_name.lower() == "coberlin":
        events = Event.query.filter_by(source_id=2).all()
    else:
        return render_template("error.html")
    return render_template("service_name.html", data=events)


@main.route("/date/<event_date>", methods=["GET"])  ### YYYY-MM-DD
def dates(event_date):
    formatted_date = datetime.strptime(event_date, "%Y-%m-%d")
    formatted_date = date(
        formatted_date.year, formatted_date.month, formatted_date.day
    ).isoformat()
    events = Event.query.filter_by(event_start=formatted_date).all()
    return render_template("event_date.html", data=events)
