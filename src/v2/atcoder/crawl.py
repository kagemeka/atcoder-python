import typing

import aiohttp


async def request_get(
    url: str,
    session: typing.Optional[aiohttp.ClientSession] = None,
) -> aiohttp.client_reqrep.ClientResponse:
    if session is None:
        session = aiohttp.ClientSession()
    with session:
        return await session.get(url)


async def request_post(url: str, payload: typing.Dict) -> None:
    ...
