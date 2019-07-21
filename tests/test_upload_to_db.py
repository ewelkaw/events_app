import unittest
from app import create_app, db
from app.model import WebSource, Event
from upload_data_to_db import prepare_keys, upload_services, upload_events
from flask import current_app


class DBTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app("development")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config["TESTING"])

    def test_prepare_keys(self):
        keys = ["TestDataTest", "NewDataTest"]
        new_keys = {"TestDataTest": "Test", "NewDataTest": "New"}
        assert new_keys == prepare_keys(keys)

    def test_upload_services(self):
        new_keys = {"TestDataTest": "Test", "NewDataTest": "New"}
        new_servs = upload_services(new_keys)
        db.session.commit()
        assert isinstance(new_servs["TestDataTest"], WebSource)
        assert new_servs["TestDataTest"].source_name == "Test"
        assert len(list(new_servs.keys())) == len(list(new_keys.keys()))
        with db.session.no_autoflush:
            sources = db.session.query(WebSource).count()
            assert sources == 2

    def test_upload_events(self):
        data = {
            "TestDataTest": [
                {"name": "TestEvent", "date": ["2019-03-07", "2019-05-07"]},
                {"name": "TestEvent2", "date": ["2018-12-06"]},
            ],
            "TestTestDataTest": [
                {"name": "TestEventTest", "date": ["2019-02-17", "2019-03-17"]}
            ],
        }
        services_objects_map = upload_services(
            {"TestDataTest": "Test", "TestTestDataTest": "TestTest"}
        )
        upload_events(data, services_objects_map)
        db.session.commit()
        with db.session.no_autoflush:
            events = db.session.query(Event).count()
            assert events == 3
