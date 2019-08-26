import unittest
from app import create_app, db
from app.models import WebSource, Event
from sqlalchemy.orm import sessionmaker
from datetime import datetime


class FlaskClientDifferentWebSourcesTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.session = sessionmaker()
        db.create_all()
        self.source_1 = WebSource(source_name="test1")
        self.source_2 = WebSource(source_name="test2")
        self.date_start = datetime(2019, 7, 2)
        self.date_start_2 = datetime(2019, 7, 4)
        self.date_end = datetime(2019, 8, 2)
        self.event_1 = Event(
            event_name="test_event_1",
            event_start=self.date_start,
            event_end=self.date_end,
            source=self.source_1,
        )
        self.event_2 = Event(
            event_name="test_event_2",
            event_start=self.date_start_2,
            event_end=self.date_end,
            source=self.source_1,
        )
        self.event_3 = Event(
            event_name="test_event_3", event_start=self.date_start, source=self.source_2
        )
        db.session.add_all(
            [self.source_1, self.source_2, self.event_1, self.event_2, self.event_3]
        )
        db.session.commit()
        self.client = self.app.test_client(use_cookies=False)

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_index_events(self):
        response = self.client.get("/")
        print("data", response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            lambda x: x in response.get_data(as_text=True),
            ["test_event_1", "test_event_2", "test_event_3"],
        )
        self.assertTrue(
            lambda x: "/date/{}".format(x.strftime("%Y-%m-%d"))
            in response.get_data(as_text=True),
            [self.date_start, self.date_start_2],
        )
        self.assertTrue(
            "{}".format(self.date_end.strftime("%Y-%m-%d"))
            in response.get_data(as_text=True)
        )

    def test_events_for_service_1(self):
        response = self.client.get("service/test1")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            lambda x: x in response.get_data(as_text=True),
            ["test_event_1", "test_event_2"],
        )
        self.assertTrue("test_event_3" not in response.get_data(as_text=True))
        self.assertTrue(
            lambda x: "/date/{}".format(x.strftime("%Y-%m-%d"))
            in response.get_data(as_text=True),
            [self.date_start, self.date_start_2],
        )
        self.assertTrue(
            "{}".format(self.date_end.strftime("%Y-%m-%d"))
            in response.get_data(as_text=True)
        )
        self.assertTrue(
            "/date/{}".format(self.date_end.strftime("%Y-%m-%d"))
            not in response.get_data(as_text=True)
        )

    def test_events_for_service_2(self):
        response = self.client.get("service/test2")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            lambda x: x not in response.get_data(as_text=True),
            ["test_event_1", "test_event_2"],
        )
        self.assertTrue("test_event_3" in response.get_data(as_text=True))
        self.assertTrue(
            lambda x: "/date/{}".format(x.strftime("%Y-%m-%d"))
            in response.get_data(as_text=True),
            [self.date_start, self.date_start_2],
        )
        self.assertTrue(
            "{}".format(self.date_end.strftime("%Y-%m-%d"))
            not in response.get_data(as_text=True)
        )

    def test_events_for_date_1(self):
        response = self.client.get(
            "date/{}".format(self.date_start.strftime("%Y-%m-%d"))
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            lambda x: x in response.get_data(as_text=True),
            ["test_event_1", "test_event_3"],
        )
        self.assertTrue("test_event_2" not in response.get_data(as_text=True))
        self.assertTrue(
            "/date/{}".format(self.date_end.strftime("%Y-%m-%d"))
            not in response.get_data(as_text=True)
        )
        self.assertTrue(
            "{}".format(self.date_end.strftime("%Y-%m-%d"))
            in response.get_data(as_text=True)
        )

    def test_events_for_date_2(self):
        response = self.client.get(
            "date/{}".format(self.date_start_2.strftime("%Y-%m-%d"))
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            lambda x: x not in response.get_data(as_text=True),
            ["test_event_1", "test_event_3"],
        )
        self.assertTrue("test_event_2" in response.get_data(as_text=True))
        self.assertTrue(
            "/date/{}".format(self.date_end.strftime("%Y-%m-%d"))
            not in response.get_data(as_text=True)
        )
        self.assertTrue(
            "{}".format(self.date_end.strftime("%Y-%m-%d"))
            in response.get_data(as_text=True)
        )


if __name__ == "__main__":
    unittest.main()
