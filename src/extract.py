import json
from pathlib import Path
from urllib.parse import urljoin

import requests
import truststore

from src.config import (
    NORTHWIND_BASE_URL,
    NORTHWIND_ENTITIES,
    RAW_NORTHWIND_DIR,
    RAW_RIKSBANK_DIR,
    RIKSBANK_RATE_URLS,
)


truststore.inject_into_ssl()


def fetch_json(url: str) -> object:
    response = requests.get(url, timeout=60)
    response.raise_for_status()
    return response.json()


def fetch_odata_collection(url: str) -> dict[str, object]:
    data = fetch_json(url)
    if not isinstance(data, dict):
        raise TypeError(f"Expected OData response object from {url}")

    values = list(data.get("value", []))
    next_link = data.get("@odata.nextLink")

    while next_link:
        next_url = urljoin(f"{NORTHWIND_BASE_URL}/", next_link)
        next_data = fetch_json(next_url)
        if not isinstance(next_data, dict):
            raise TypeError(f"Expected OData response object from {next_url}")
        values.extend(next_data.get("value", []))
        next_link = next_data.get("@odata.nextLink")

    return {
        "@odata.context": data.get("@odata.context"),
        "value": values,
    }


def save_json(data: object, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def extract_northwind() -> None:
    for file_stem, entity in NORTHWIND_ENTITIES.items():
        url = f"{NORTHWIND_BASE_URL}/{entity}"
        print(f"Fetching {url}")
        save_json(fetch_odata_collection(url), RAW_NORTHWIND_DIR / f"{file_stem}.json")


def extract_riksbank() -> None:
    for year, url in RIKSBANK_RATE_URLS.items():
        print(f"Fetching {url}")
        save_json(fetch_json(url), RAW_RIKSBANK_DIR / f"exchange_rates_{year}.json")


def extract_all() -> None:
    extract_northwind()
    extract_riksbank()


if __name__ == "__main__":
    extract_all()