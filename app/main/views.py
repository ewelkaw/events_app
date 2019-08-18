from datetime import date, datetime

from flask import render_template
from sqlalchemy import func

from app import db

from ..model import Event, WebSource
from . import main


@main.route("/", methods=["GET"])
def index():
    events = Event.query.all()
    return render_template("index.html", events=events)


@main.route("/service/<service_name>/", methods=["GET"])
@main.route("/service/<service_name>", methods=["GET"])  # berghain, co-berlin
def services(service_name):
    events = (
        db.session.query(Event, WebSource)
        .filter(Event.source_id == WebSource.id)
        .filter(func.lower(WebSource.source_name) == service_name.lower())
        .with_entities(Event)
        .all()
    )
    return render_template(
        "service_name.html", events=events, service_name=service_name
    )


@main.route("/date/<event_date>/", methods=["GET"])  ### YYYY-MM-DD
@main.route("/date/<event_date>", methods=["GET"])  ### YYYY-MM-DD
def dates(event_date):
    formatted_date = datetime.strptime(event_date, "%Y-%m-%d")
    formatted_date = date(
        formatted_date.year, formatted_date.month, formatted_date.day
    ).isoformat()
    events = Event.query.filter_by(event_start=formatted_date).all()
    return render_template("event_date.html", events=events, event_date=event_date)
