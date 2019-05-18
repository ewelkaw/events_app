import pytest
import os
from urllib3_mock import Responses
from pathlib import Path
from data_scrapping.data_scrapping import (
    Fetcher,
    CoBerlinDataFetcher,
    Parser,
    Scrapper,
    FileReader,
)

responses = Responses("requests.packages.urllib3")


class MockExternalFetcher:
    def __init__(self, http_method, link, response):
        self.http_method = http_method
        self.link = link
        self.response = response

    @property
    def data(self):
        return self.response

    def request(self, http_method, link):
        if http_method == self.http_method and link == self.link:
            return self


class MockBeautifulSoup:
    def __init__(self, raw_data, features):
        self.raw_data = raw_data
        self.features = features


class MockFetcher:
    def __init__(self, link):
        self.link = link

    @property
    def download_data(self):
        return self.link


class MockParser:
    def __init__(self, fetched_data):
        self.fetched_data = fetched_data

    @property
    def parse_raw_data(self):
        return self.fetched_data


class TestFetcher(object):
    def test_downloading_data(self):
        link = "http://events/"
        custom_fetcher = MockExternalFetcher("GET", link, "<!DOCTYPE ")
        response = Fetcher(link, http=custom_fetcher).download_data
        assert response == "<!DOCTYPE "


class TestCoBerlinDataFetcher(object):
    @pytest.fixture
    def coberlin_html(self):
        path = os.path.dirname(os.path.abspath(__file__))
        coberlin_html = open(Path(path, "fixtures/coberlin.html"), "r")
        return coberlin_html.read()

    def test_prepare_all_pages(self, coberlin_html):
        link = "http://events/"
        link2 = "http://events/?page=1"
        custom_fetcher = MockExternalFetcher("GET", link, coberlin_html)
        pages = CoBerlinDataFetcher(link, custom_fetcher).prepare_all_pages
        assert pages == [link, link2]


class TestParser(object):
    @pytest.fixture
    def raw_data(self):
        return "<!DOCTYPE "

    def test_parser(self, raw_data):
        result = Parser(raw_data, MockBeautifulSoup).parse_raw_data
        assert isinstance(result, MockBeautifulSoup)
        assert result.raw_data == raw_data
        assert result.features == "html.parser"


class TestScrapper(object):
    def test_scrapper(self):
        link = "http://"
        result = Scrapper(link, MockFetcher, MockParser).parsed_data
        assert result == link


class TestFileReader(object):
    def test_reader(self):
        expected_result = [
            {"TestingDataStandarizer": ["http://test/", None]},
            {"Testing2DataStandarizer": ["http://test2/", "CustomDataFetcher"]},
        ]

        file_path = "tests/fixtures/data.yml"
        data = FileReader(file_path).data
        assert len(data["services"]) == 2
        assert data["services"] == expected_result
