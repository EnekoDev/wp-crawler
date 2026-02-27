import os
import requests
import json

from dotenv import load_dotenv
from bs4 import BeautifulSoup
from urllib.parse import urljoin

load_dotenv()

SITE_URL = os.getenv('SITE_URL')
API_URL = '/wp-json/wp/v2'
QUERY = "/posts?_fields=link&per_page=100"

def get_pages():
    pages = set()
    req = SITE_URL + API_URL + QUERY
    try:
        res = requests.get(req, timeout=10)
        res.raise_for_status()
        if res.ok:
            data = res.json()
            for obj in data:
                pages.add(obj['link'])
    except requests.exceptions.ConnectionError as exc:
        print(exc)
    return pages

def get_page_links(url):
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
    except requests.exceptions.ConnectionError as exc:
        print(exc)
        return {url: []}
    
    soup = BeautifulSoup(res.text, "html.parser")
    links = set()

    links.add(url)
    for tag in soup.find_all("a", href=True):
        href = tag["href"]
        absolute_url = urljoin(url, href)
        links.add(absolute_url)
    
    return {url: sorted(list(links))}

def writeJson(data, filename="output/output.json"):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            existing_data = json.load(f)
    else:
        existing_data = {}
    
    existing_data.update(data)
    
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=4)