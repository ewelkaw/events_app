from abc import ABC, abstractmethod
from datetime import datetime, date

from bs4 import BeautifulSoup


class DataStandarizer(ABC):
    def __init__(self, data: BeautifulSoup):
        self.data = data

    @abstractmethod
    def cleaned_raw_data(self):
        pass


class BerghainDataStandarizer(DataStandarizer):
    def __init__(self, data: BeautifulSoup):
        super().__init__(data)
        self._cleaned_raw_data: list = []

    @property
    def cleaned_raw_data(self):
        # remember this may be recalculated on each calling
        # which maybe (or may not be) a bottleneck later
        self._cleaned_raw_data = self.data.findAll(attrs={"class": "x3cols"})
        self._cleaned_raw_data = self._cleaned_raw_data[0].findAll("a")
        self._cleaned_raw_data = self._prepare_rows()
        return self._cleaned_raw_data

    # private method, need to use it with self
    def _prepare_rows(self):
        rows = []
        for row in self._cleaned_raw_data:
            event_date = self._prepare_date(row.contents[0].strip()[4:])
            name = row.findAll("span")[0].contents[0]
            rows.append({"date": [event_date], "name": name})
        return rows

    def _prepare_date(self, raw_date):
        formatted_date = datetime.strptime(raw_date, "%d %b %Y").date().isoformat()
        return formatted_date  # YYYY-MM-DD


class CoBerlinDataStandarizer(DataStandarizer):
    def __init__(self, data: BeautifulSoup):
        super().__init__(data)
        self._cleaned_raw_data: list = []

    @property
    def cleaned_raw_data(self):
        # remember this may be recalculated on each calling
        # which maybe (or may not be) a bottleneck later
        self._cleaned_raw_data = self.data.findAll(attrs={"class": "calender-text"})
        self._cleaned_raw_data = self._prepare_rows()
        return self._cleaned_raw_data

    # private method
    def _prepare_rows(self):
        data = []
        for i in self._cleaned_raw_data:
            data.append(
                [
                    i.findAll(attrs={"class": "article-title"})[0],
                    i.findAll(attrs={"class": "article-date"})[0],
                ]
            )

        rows = []
        for row in data:
            name = row[0].text
            event_date = row[1].text
            if "to" in event_date:
                event_date = event_date.split(" to ")
            else:
                event_date = [event_date]
            event_date = self._prepare_date(event_date)
            rows.append({"date": event_date, "name": name})
        return rows

    def _prepare_date(self, raw_date):
        formatted_date = []
        for i in raw_date:
            i = datetime.strptime(i, "%d/%m/%y")
            formatted_date.append(date(i.year, i.month, i.day).isoformat())
        return formatted_date  # YYYY-MM-DD


def standarize_data(raw_data: dict) -> dict:
    standarized_data: dict = {}
    services_keys = list(raw_data.keys())

    for key in services_keys:
        standarized_data[key] = []
        for page in raw_data[key]:
            standarized_data[key].extend(eval(key)(page).cleaned_raw_data)
        print("##### standarized_data {} #####".format(key), standarized_data[key])
    return standarized_data
