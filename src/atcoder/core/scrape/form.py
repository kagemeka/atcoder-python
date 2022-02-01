import typing

import bs4


async def scrape_csrf_token_in_form(
    form: bs4.element.Tag,
) -> typing.Optional[str]:
    section = form.find(attrs={"name": "csrf_token"})
    if section is None:
        return None
    return typing.cast(
        str,
        section.get("value"),
    )
