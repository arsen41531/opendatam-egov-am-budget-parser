#!/usr/bin/env python

import datetime
import logging
from pathlib import Path

import pandas as pd
import requests

NOW = datetime.datetime.now()
CURRENT_YEAR = NOW.year
CURRENT_DATE = NOW.strftime("%Y-%m-%d")
BASE_URL = "https://www.e-gov.am"
XML_FILES = [
    "GOV_BUDGET.XML",
    "GOV_CONTR.XML",
    "GOV_GROUP.XML",
    "GOV_CONTR_F.XML",
    "GOV_ITEM.XML",
    "GOV_MIN.XML",
]

logging.basicConfig(
    format="%(asctime)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S", level=logging.INFO
)


def fetch_gov_budget_data(year: int, xml_file: str) -> pd.DataFrame:
    """Fetches data from e-gov.am in a form of XML files"""

    url_prefix = f"{BASE_URL}/budget_archive/{str(year)}/data"

    # for current year, data is in a different location
    if year == CURRENT_YEAR:
        url_prefix = f"{BASE_URL}/interactive/data"

    # some servers block requests with default user agent
    # fake user agent to avoid this
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(f"{url_prefix}/{xml_file}", headers=headers)

    return pd.read_xml(response.text, xpath=".//ROW")


if __name__ == "__main__":
    for year in range(2016, CURRENT_YEAR + 1):
        if year == 2018:
            # data for 2018 is not available
            logging.info(f"Skipping {year}...")
            continue

        data_folder = Path.joinpath(Path.cwd(), "_data", CURRENT_DATE)
        data_folder.mkdir(exist_ok=True)
        for xml_file in XML_FILES:
            logging.info(f"Fetching {xml_file} for {year}...")
            contents = fetch_gov_budget_data(year, xml_file)

            csv_filename = Path(f"{year}-{xml_file.lower()}").with_suffix(".csv")
            csv_filepath = Path.joinpath(data_folder, csv_filename)
            logging.info(f"Writing {csv_filename}...")
            csv_filepath.write_text(contents.to_csv(index=False))

            json_filename = Path(f"{year}-{xml_file.lower()}").with_suffix(".json")
            json_filepath = Path.joinpath(data_folder, json_filename)
            logging.info(f"Writing {json_filename}...")
            json_filepath.write_text(
                contents.to_json(orient="records", force_ascii=False, indent=2)
            )
