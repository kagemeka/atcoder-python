import typing

import bs4


async def parse_html(html_text: bytes) -> bs4.BeautifulSoup:
    return bs4.BeautifulSoup(html_text, "html.parser")


def _strip_unit(measured_value: str) -> int:
    # strip unit like "ms" or "kB"
    return int(measured_value.split()[0])


async def _scrape_html_options(
    html: bytes,
    id_in_html: str,
) -> typing.Optional[typing.List[str]]:
    soup = await parse_html(html)
    section = soup.find("select", id=id_in_html)
    if section is None:
        return None
    return list(
        map(
            typing.cast(
                typing.Callable[[bs4.element.Tag], str],
                lambda element: element.get("value"),
            ),
            section.find_all("option")[1:],
        )
    )
