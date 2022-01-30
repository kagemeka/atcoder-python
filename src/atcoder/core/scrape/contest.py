from atcoder.core.contest import Contest
from atcoder.core.scrape.utils import parse_html


async def scrape_contest(html: bytes) -> Contest:
    soup = await parse_html(html)
    section = soup.find(class_="contest-title")
    return Contest(
        id=section.get("href").split("/")[-1],
        title=section.text,
    )
