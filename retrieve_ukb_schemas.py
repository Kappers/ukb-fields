"""
Download reference UK Biobank schemas, saves to schemas/SCHEMA_DESCRIPTION(.YYYYMMDD).txt 

See: https://biobank.ndph.ox.ac.uk/showcase/download.cgi
"""

__author__ = "Thomas Kaplan"

import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime

BIOBANK_DOMAIN = "https://biobank.ndph.ox.ac.uk"
SCHEMA_URL = f"{BIOBANK_DOMAIN}/showcase/download.cgi"


def _get_schema_dl_url(schema_i):
    return f"{BIOBANK_DOMAIN}/ukb/scdown.cgi?fmt=txt&id={schema_i}"


if __name__ == "__main__":

    yyyymmdd = datetime.today().strftime("%Y%m%d")

    page = requests.get(SCHEMA_URL)
    soup = BeautifulSoup(page.content, "html.parser")
    is_schema_link = lambda href: href is not None and "schema.cgi?id=" in href
    schema_links = soup.find_all("a", href=is_schema_link)

    for link in schema_links:
        desc = "_".join([d for d in link.text.lower().split() if d])
        schema_i = re.search(r"\d+", link["href"]).group()
        schema_url = _get_schema_dl_url(schema_i)
        response = requests.get(schema_url)

        print(f"Writing schema {schema_i} (dates {yyyymmdd} and undated)")

        with open(f"schemas/{desc}.{yyyymmdd}.txt", "wb") as file:
            file.write(response.content)

        with open(f"schemas/{desc}.txt", "wb") as file:
            file.write(response.content)
