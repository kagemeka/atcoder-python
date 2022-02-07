from atcoder.constant import _SITE_URL
import aiohttp
import dataclasses
import datetime
import enum
import typing
import bs4
import atcoder.scrape
import logging

_LOGGER = logging.getLogger(__name__)

_CONTESTS_URL = f"{_SITE_URL}/contests"
_CONTESTS_ARCHIVE_URL = f"{_CONTESTS_URL}/archive"
_LANGUAGE = "ja"


class _AlgorithmType(enum.Enum):
    DEFINITE = enum.auto()
    HEURISTIC = enum.auto()


class Color(enum.Enum):
    GREEN = enum.auto()
    BLUE = enum.auto()
    ORANGE = enum.auto()
    RED = enum.auto()


_COLOR_FROM_STRING = {
    "user-green": Color.GREEN,
    "user-blue": Color.BLUE,
    "user-orange": Color.ORANGE,
    "user-red": Color.RED,
}


def _color_from_string(color: str) -> typing.Optional[Color]:
    return _COLOR_FROM_STRING.get(color)


class Status(enum.Enum):
    RUNNING = enum.auto()
    PERMANENT = enum.auto()
    UPCOMING = enum.auto()
    FINISHED = enum.auto()


@dataclasses.dataclass(frozen=False)
class Contest:
    id: str
    title: str
    status: typing.Optional[Status] = None
    color: typing.Optional[Color] = None
    start_datetime: typing.Optional[datetime.datetime] = None
    duration: typing.Optional[datetime.timedelta] = None


async def _get_contest_page(
    contest_id: str,
) -> aiohttp.ClientResponse:
    url = f"{_CONTESTS_URL}/{contest_id}"
    async with aiohttp.ClientSession() as session:
        _LOGGER.info(f"get {url}")
        return await session.get(url)


async def _get_archive_page(
    page: int,
) -> aiohttp.ClientResponse:
    async with aiohttp.ClientSession() as session:
        _LOGGER.info(f"get {_CONTESTS_ARCHIVE_URL}, page: {page}")
        return await session.get(
            url=_CONTESTS_ARCHIVE_URL,
            params={
                "page": page,
                "lang": _LANGUAGE,
            },
        )


async def _get_contests_page() -> aiohttp.ClientResponse:
    async with aiohttp.ClientSession() as session:
        _LOGGER.info(f"get {_CONTESTS_URL}")
        return await session.get(
            _CONTESTS_URL,
            params={"lang": _LANGUAGE},
        )


# def _scrape_contest(html: str) -> Contest:
#     soup = atcoder.scrape._parse_html(html)
#     section = soup.find(class_="contest-title")
#     return Contest(
#         id=section.get("href").split("/")[-1],
#         title=section.text,
#     )


def _parse_duration(duration: str) -> datetime.timedelta:
    hours, minutes = map(int, duration.split(":"))
    return datetime.timedelta(hours=hours, minutes=minutes)


def _scrape_row(row: bs4.element.Tag) -> Contest:
    infos = row.find_all("td")
    color_texts = infos[1].span.get("class")
    color = None if not color_texts else _color_from_string(color_texts[0])
    return Contest(
        id=infos[1].a.get("href").split("/")[-1],
        title=infos[1].a.text.strip(),
        color=color,
        start_datetime=datetime.datetime.strptime(
            infos[0].time.text,
            "%Y-%m-%d %H:%M:%S%z",
        ),
        duration=_parse_duration(infos[2].text),
    )


async def _scrape_running_contests(
    html: str,
) -> typing.AsyncIterator[Contest]:
    soup = atcoder.scrape._parse_html(html)
    section = soup.find(id="contest-table-action")
    if section is None:
        return
    for row in section.table.tbody.find_all("tr"):
        contest = _scrape_row(row)
        contest.status = Status.RUNNING
        yield contest


async def _scrape_permanent_contests(
    html: str,
) -> typing.AsyncIterator[Contest]:
    async def scrape_row(row: bs4.element.Tag) -> Contest:
        infos = row.find_all("td")
        color_texts = infos[0].span.get("class")
        color = None if not color_texts else _color_from_string(color_texts[0])
        return Contest(
            id=infos[0].a.get("href").split("/")[-1],
            title=infos[0].a.text.strip(),
            status=Status.PERMANENT,
            color=color,
        )

    soup = atcoder.scrape._parse_html(html)
    section = soup.find(id="contest-table-permanent")
    if section is None:
        return
    for row in section.table.tbody.find_all("tr"):
        yield await scrape_row(row)


async def _scrape_upcoming_contests(
    html: str,
) -> typing.AsyncIterator[Contest]:
    soup = atcoder.scrape._parse_html(html)
    section = soup.find(id="contest-table-upcoming")
    if section is None:
        return
    for row in section.table.tbody.find_all("tr"):
        contest = _scrape_row(row)
        contest.status = Status.UPCOMING
        yield contest


def _scrape_pagination(html: str) -> typing.Tuple[int, int]:
    soup = atcoder.scrape._parse_html(html)
    pagination = soup.find(class_="pagination")
    current = int(pagination.find(class_="active").text)
    last = int(pagination.find_all("li")[-1].text)
    return current, last


async def _scrape_finished_contests(
    html: str,
) -> typing.AsyncIterator[Contest]:
    soup = atcoder.scrape._parse_html(html)
    if soup.table is None:
        return
    for row in soup.table.tbody.find_all("tr"):
        contest = _scrape_row(row)
        contest.status = Status.FINISHED
        yield contest


async def _get_archive_pages() -> typing.AsyncIterator[aiohttp.ClientResponse]:
    response = await _get_archive_page(1)
    _, last_page = _scrape_pagination(await response.text())
    get_pages = [
        asyncio.create_task(_get_archive_page(i))
        for i in range(1, last_page + 1)
    ]
    # for response in await asyncio.gather(*get_pages):
    #     yield response
    for get_page in get_pages:
        yield await get_page


async def fetch_all_contests() -> typing.AsyncIterator[Contest]:
    get = asyncio.create_task(_get_contests_page())
    async for response in _get_archive_pages():
        async for contest in _scrape_finished_contests(await response.text()):
            yield contest
    html = await (await get).text()
    async for contest in _scrape_upcoming_contests(html):
        yield contest
    async for contest in _scrape_running_contests(html):
        yield contest
    async for contest in _scrape_permanent_contests(html):
        yield contest


async def fetch_contest_details() -> None:
    ...


async def register() -> None:
    ...



if __name__ == "__main__":
    _LOGGING_FORMAT = "%(asctime)s %(levelname)s %(pathname)s %(message)s"
    logging.basicConfig(
        format=_LOGGING_FORMAT,
        datefmt="%Y-%m-%d %H:%M:%S%z",
        handlers=[logging.StreamHandler()],
        level=logging.DEBUG,
    )    
    import asyncio

    async def test() -> None:
        contests = []
        async for contest in fetch_all_contests():
            contests.append(contest)
        print(len(contests))

    import time

    s = time.time()

    asyncio.run(test())
    print(time.time() - s)
