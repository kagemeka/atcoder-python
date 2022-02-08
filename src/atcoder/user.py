import logging

import aiohttp

import atcoder.constant

USERS_URL = f"{atcoder.constant._SITE_URL}/users"

_LOGGER = logging.getLogger(__name__)


async def _get_user_profile_page(
    session: aiohttp.ClientSession,
    user_id: str,
) -> aiohttp.ClientResponse:
    url = f"{USERS_URL}/{user_id}"
    _LOGGER.info(f"get {url}")
    return await session.get(url)


async def _get_user_competition_history_page(
    session: aiohttp.ClientSession,
    user_id: str,
) -> aiohttp.ClientResponse:
    url = f"{USERS_URL}/{user_id}/history"
    _LOGGER.info(f"get {url}")
    return await session.get(url)
