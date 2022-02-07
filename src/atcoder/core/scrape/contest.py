# from atcoder.core.contest import Contest
# from atcoder.core.scrape.utils import _parse_html


# async def scrape_contest(html: bytes) -> Contest:
#     soup = _parse_html(html)
#     section = soup.find(class_="contest-title")
#     return Contest(
#         id=section.get("href").split("/")[-1],
#         title=section.text,
#     )
