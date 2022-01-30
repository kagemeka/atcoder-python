import bs4


async def parse_html(html_text: bytes) -> bs4.BeautifulSoup:
    return bs4.BeautifulSoup(html_text, "html.parser")


def _strip_unit(measured_value: str) -> int:
    # strip unit like "ms" or "kB"
    return int(measured_value.split()[0])
