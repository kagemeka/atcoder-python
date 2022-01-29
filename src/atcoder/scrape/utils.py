import bs4


async def parse_html(html_text: bytes) -> bs4.BeautifulSoup:
    return bs4.BeautifulSoup(html_text, "html.parser")
