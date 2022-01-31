import requests


async def fetch_page_source(url: str) -> bytes:
    return requests.get(url).content
