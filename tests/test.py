import aiohttp
import asyncio
import time

import logging

logger = logging.getLogger(__name__)
import bs4


async def get(session, url: str, i) -> str:
    logger.debug(i)
    return await session.get(url)
    # async with session.get(url) as response:
        # text = await response.text()
        # logger.debug(f"{i} end")
        # return text


N = 10
URL = "https://atcoder.jp"
# URL = "https://kenkoooo.com/atcoder/atcoder-api/v3/language_list"


async def sub(i: int) -> str:
    async with aiohttp.ClientSession() as session:
        task = asyncio.create_task((get(session, URL, i)))
        return await task


async def main() -> None:
    tasks = []
    for i in range(N):
        tasks.append(asyncio.create_task(sub(i)))
    contents = await asyncio.gather(*tasks)
    print(type(contents[0]))
    # for content in contents:


# async def main() -> None:
#     async with aiohttp.ClientSession() as session:
#         tasks = []
#         for i in range(N):
#             tasks.append(asyncio.create_task(get(session, URL, i)))
#         contents = await asyncio.gather(*tasks)
#         # for content in contents:
#         soup = bs4.BeautifulSoup(contents[0], 'html.parser')
#         print(soup.prettify())
#         # break
#             # ...
#         # content = contents[0]
#         session.cookie_jar.save('cookies.json')
#         for cookie in session.cookie_jar:
#             print(cookie.key)
#         # filtered = session.cookie_jar.filter_cookies('atcoder.jp/')
#         # print(filtered.save('cookies.json'))
#         print(session.cookie_jar)


LOGGING_FORMAT = "%(asctime)s %(levelname)s %(pathname)s %(message)s"
logging.basicConfig(
    format=LOGGING_FORMAT,
    datefmt="%Y-%m-%d %H:%M:%S%z",
    handlers=[logging.StreamHandler()],
    level=logging.DEBUG,
)

s = time.time()
asyncio.run(main())
print(time.time() - s)

import requests


def main2() -> None:
    for _ in range(N):
        response = requests.get(URL)
        print(response.cookies)


# s = time.time()
# main2()
# print(time.time() - s)
