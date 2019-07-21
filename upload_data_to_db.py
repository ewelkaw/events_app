import datetime
from pathlib import Path

from app import db, create_app
from app.model import Event, WebSource
from data_scraping.data_cleaning import standarize_data
from data_scraping.data_scraping import prepare_data_from_each_service

services_file = Path(__file__).absolute().parent.joinpath("data_scraping/services.yml")


def add_data_to_db():
    app = create_app("development")
    app_context = app.app_context()
    app_context.push()
    db.drop_all()
    db.create_all()

    data = get_data()
    keys = list(data.keys())
    services_objects_map = upload_services(prepare_keys(keys))
    upload_events(data, services_objects_map)
    db.session.commit()


def get_data() -> dict:
    scrapped_data = prepare_data_from_each_service(services_file)
    return standarize_data(scrapped_data)


def prepare_keys(keys: list) -> dict:
    services_names_map = {}
    for key in keys:
        services_names_map[key] = key.split("Data")[0]
    return services_names_map


def upload_services(services_names: dict) -> dict:
    services_objects_map = {}
    for key, value in services_names.items():
        value = WebSource(source_name=value)
        db.session.add(value)
        services_objects_map[key] = value
    return services_objects_map


def upload_events(data: dict, services_objects_map: dict):
    for key, values in data.items():
        service = services_objects_map[key]
        for value in values:
            event_dates = value.get("date")
            event_dates = [
                datetime.date(*map(lambda x: int(x), event_date.split("-")))
                for event_date in event_dates
            ]
            if len(event_dates) == 2:
                event = Event(
                    event_name=value.get("name"),
                    event_start=event_dates[0],
                    event_end=event_dates[1],
                    source=service,
                )
            else:
                event = Event(
                    event_name=value.get("name"),
                    event_start=event_dates[0],
                    source=service,
                )
            db.session.add(event)


if __name__ == "__main__":
    add_data_to_db()
