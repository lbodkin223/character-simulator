"""Fetch a comic book character from the ComicVine API and save as JSON."""
import json
import os
from pathlib import Path
from typing import Dict, Optional

import requests

API_KEY_ENV = "COMICVINE_API_KEY"
BASE_URL = "https://comicvine.gamespot.com/api"
HEADERS = {"User-Agent": "character-simulator"}


def search_character(name: str) -> Optional[Dict]:
    """Search ComicVine for a character and return the first match details."""
    api_key = os.getenv(API_KEY_ENV)
    if not api_key:
        print(f"Please set the {API_KEY_ENV} environment variable with your API key.")
        return None

    params = {
        "api_key": api_key,
        "format": "json",
        "resources": "character",
        "query": name,
    }
    resp = requests.get(f"{BASE_URL}/search/", params=params, headers=HEADERS)
    resp.raise_for_status()
    results = resp.json().get("results", [])
    if not results:
        print("No character found matching that name.")
        return None
    detail_url = results[0].get("api_detail_url")
    if not detail_url:
        print("Character result missing detail URL.")
        return None
    detail_resp = requests.get(detail_url, params={"api_key": api_key, "format": "json"}, headers=HEADERS)
    detail_resp.raise_for_status()
    return detail_resp.json().get("results")


def save_character(data: Dict, name: str) -> Path:
    """Save the character data to the characters folder."""
    slug = name.lower().replace(" ", "_")
    path = Path("characters") / f"{slug}.json"
    path.parent.mkdir(exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    return path


def main() -> None:
    name = input("Enter character name: ").strip()
    if not name:
        print("No name provided.")
        return
    details = search_character(name)
    if not details:
        return
    char_data = {
        "name": details.get("name"),
        "real_name": details.get("real_name"),
        "aliases": details.get("aliases"),
        "description": details.get("deck"),
        "powers": [p.get("name") for p in details.get("powers", [])],
    }
    file_path = save_character(char_data, name)
    print(f"Saved character to {file_path}")


if __name__ == "__main__":
    main()
