import typing

import bs4


def _parse_html(html: str) -> bs4.BeautifulSoup:
    return bs4.BeautifulSoup(html, "html.parser")


def _strip_unit(measured_value: str) -> int:
    # strip unit like "ms" or "kB"
    return int(measured_value.split()[0])


def _scrape_html_options(
    html: str,
    id_in_html: str,
) -> typing.Optional[typing.List[str]]:
    soup = _parse_html(html)
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


def _scrape_csrf_token_in_form(
    form: bs4.element.Tag,
) -> typing.Optional[str]:
    section = form.find(attrs={"name": "csrf_token"})
    if section is None:
        return None
    return typing.cast(
        str,
        section.get("value"),
    )
