import argparse
from pathlib import Path

import urllib3
import yaml
from bs4 import BeautifulSoup

from .data_cleaning import standarize_data


class FileReader:
    def __init__(self, file_path: str):
        self.file_path = file_path

    @property
    def data(self):
        with open(Path.cwd() / self.file_path) as file:
            return yaml.load(file, Loader=yaml.FullLoader)


class Fetcher:
    def __init__(self, service_link: str, http=urllib3.PoolManager()):
        self.service_link = service_link
        self.http = http

    # method works as property
    @property
    def download_data(self):
        response = self.http.request("GET", self.service_link)
        return response.data


class CoBerlinDataFetcher(Fetcher):
    @property
    def prepare_all_pages(self) -> list:
        services_links = []
        response = self.download_data
        response = BeautifulSoup(response, features="html.parser")
        pages_data = response.findAll(attrs={"class": "arrow last"})
        pages_data = pages_data[0].findAll("a")[0].get("href").split("page=")
        last_page_number = int(pages_data[-1]) + 1
        for i in range(last_page_number):
            if i == 0:
                services_links.append(self.service_link)
            else:
                services_links.append(self.service_link + "?page=" + str(i))
        return services_links


class Parser:
    def __init__(self, raw_data: str, actual_parser=BeautifulSoup):
        self.raw_data = raw_data
        self.actual_parser = actual_parser

    # method works as property
    @property
    def parse_raw_data(self):
        return self.actual_parser(self.raw_data, features="html.parser")


class Scrapper:
    def __init__(self, service_link: str, fetcher=Fetcher, parser=Parser):
        self.service_link = service_link
        self.fetcher = fetcher
        self.parser = parser

    # method works as property
    @property
    def parsed_data(self):
        fetched_data = self.fetcher(self.service_link).download_data
        return self.parser(fetched_data).parse_raw_data


def prepare_data_from_each_service(
    file_path: str, scrapper=Scrapper, globals=None
) -> dict:
    data = FileReader(file_path).data

    data_from_services = {}
    for service in data["services"]:
        key = list(service.keys())[0]
        data_from_services[key] = None

        fetcher = service[key][1]
        service_links = [service[key][0]]

        if fetcher:
            service_links = eval(fetcher, globals)(service_links[0]).prepare_all_pages
        data_from_services[key] = [
            scrapper(service_link).parsed_data for service_link in service_links
        ]
    return data_from_services


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Prepare services names from yml file")
    parser.add_argument("file_name", help="file name like file_example.yml")
    args = parser.parse_args()

    if args.file_name is not None:
        scrapped_data = prepare_data_from_each_service(args.file_name)
        standarized_data = standarize_data(scrapped_data)
    else:
        print("You suposed to provide path to file with services names")
