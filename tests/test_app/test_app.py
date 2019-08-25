import unittest
from app import create_app, db
from app.models import WebSource, Event
from sqlalchemy.orm import sessionmaker
from datetime import datetime


class FlaskClientTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.session = sessionmaker()
        db.create_all()
        self.client = self.app.test_client(use_cookies=False)

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Events in Berlin!" in response.get_data(as_text=True))

    def test_service_berghain(self):
        response = self.client.get('service/berghain')
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Events for service:" in response.get_data(as_text=True))

    def test_service_co_berlin(self):
        response = self.client.get('service/co-berlin')
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Events for service:" in response.get_data(as_text=True))

    def test_date(self):
        response = self.client.get('date/2018-09-11')
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Events for date:" in response.get_data(as_text=True))


class FlaskClientDifferentWebSourcesTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.session = sessionmaker()
        self.source = WebSource(source_name="test")
        self.event = Event(event_name='test_event', event_start=datetime.now(), source=self.source)
        db.create_all()
        self.client = self.app.test_client(use_cookies=False)

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
#
#     def test_index_events(self):
#         response = self.client.get('/')
#         self.assertEqual(response.status_code, 200)
#         self.assertTrue("Events in Berlin!" in response.get_data(as_text=True))
#
#     def test_service_events(self):
#         events = Events.
#         response = self.client.get('/')
#         self.assertEqual(response.status_code, 200)
#         self.assertTrue("Events in Berlin!" in response.get_data(as_text=True))

    # def test_date_events(self):
#         events = Events.
#         response = self.client.get('/')
#         self.assertEqual(response.status_code, 200)
#         self.assertTrue("Events in Berlin!" in response.get_data(as_text=True))


if __name__ == '__main__':
    unittest.main()
