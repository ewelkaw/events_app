import os
from pathlib import Path

import pytest
from bs4 import BeautifulSoup

from data_scrapping.data_cleaning import (
    BerghainDataStandarizer,
    CoBerlinDataStandarizer,
    standarize_data,
)


class TestBerghainDataStandarizer(object):
    @pytest.fixture
    def berghain_html(self):
        path = os.path.dirname(os.path.abspath(__file__))
        berghain_html = open(Path(path, "fixtures/berghain.html"), "r")
        return berghain_html.read()

    def test_clean_all_berghain_data(self, berghain_html):
        data = BeautifulSoup(berghain_html, features="html.parser")
        standarized_data = BerghainDataStandarizer(data).cleaned_raw_data
        assert len(standarized_data) == 2
        assert standarized_data[0] == {
            "date": ["2019-05-01"],
            "name": "OSTGUT TON DER ARBEIT ",
        }
        assert standarized_data[1] == {"date": ["2019-05-02"], "name": "GIRL IN RED"}


class TestCoBerlinDataStandarizer(object):
    @pytest.fixture
    def coberlin_html(self):
        path = os.path.dirname(os.path.abspath(__file__))
        coberlin_html = open(Path(path, "fixtures/coberlin_2.html"), "r")
        return coberlin_html.read()

    def test_clean_all_coberlin_data(self, coberlin_html):
        data = BeautifulSoup(coberlin_html, features="html.parser")
        standarized_data = CoBerlinDataStandarizer(data).cleaned_raw_data
        assert len(standarized_data) == 2
        assert standarized_data[0] == {
            "date": ["2019-03-16", "2019-06-01"],
            "name": "Cortis & Sonderegger",
        }
        assert standarized_data[1] == {
            "date": ["2019-05-14"],
            "name": "Curator’s Guided Tour with Felix Hoffmann",
        }


class TestStandarizeData(object):
    @pytest.fixture
    def raw_data(self):
        path = os.path.dirname(os.path.abspath(__file__))
        berghain_html = BeautifulSoup(
            open(Path(path, "fixtures/berghain.html"), "r").read(),
            features="html.parser",
        )
        coberlin_html = BeautifulSoup(
            open(Path(path, "fixtures/coberlin_2.html"), "r").read(),
            features="html.parser",
        )
        return {
            "BerghainDataStandarizer": [berghain_html],
            "CoBerlinDataStandarizer": [coberlin_html],
        }

    def test_standarize_data(self, raw_data):
        standarized_data = standarize_data(raw_data)
        assert len(standarized_data["BerghainDataStandarizer"]) == 2
        assert len(standarized_data["CoBerlinDataStandarizer"]) == 2
        assert standarized_data["BerghainDataStandarizer"][0] == {
            "date": ["2019-05-01"],
            "name": "OSTGUT TON DER ARBEIT ",
        }
        assert standarized_data["BerghainDataStandarizer"][1] == {
            "date": ["2019-05-02"],
            "name": "GIRL IN RED",
        }
        assert standarized_data["CoBerlinDataStandarizer"][0] == {
            "date": ["2019-03-16", "2019-06-01"],
            "name": "Cortis & Sonderegger",
        }
        assert standarized_data["CoBerlinDataStandarizer"][1] == {
            "date": ["2019-05-14"],
            "name": "Curator’s Guided Tour with Felix Hoffmann",
        }
