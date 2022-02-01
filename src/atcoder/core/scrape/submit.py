import re
import typing

from atcoder.core.language import Language
from atcoder.core.scrape.form import scrape_csrf_token_in_form
from atcoder.core.scrape.utils import _scrape_html_options, parse_html
from atcoder.core.utils import unwrap


async def scrape_csrf_token(html: bytes) -> str:
    soup = await parse_html(html)
    return unwrap(await scrape_csrf_token_in_form(soup.find_all("form")[1]))


async def scrape_task_ids(html: bytes) -> typing.List[str]:
    return unwrap(await _scrape_html_options(html, "select-task"))


async def scrape_languages(html: bytes) -> typing.List[Language]:
    soup = await parse_html(html)
    form = soup.find_all("form")[1]
    section = form.find(id="select-lang").div
    languages = []
    pattern = re.compile(r"^(.+)\s+\((.+)\).*$")
    for option in section.find_all("option")[1:]:
        language_string = option.text.strip()
        match = re.match(pattern, language_string)
        assert match is not None
        language = Language(
            id=int(option.get("value")),
            name=match[1],
            version=match[2],
        )
        languages.append(language)
    return languages
