import atcoder.constant
import requests

USERS_URL = f"{atcoder.constant._SITE_URL}/users"


async def _get_user_profile_page(
    user_id: str,
) -> requests.Response:
    url = f"{USERS_URL}/{user_id}"
    return requests.get(url)


async def _get_user_competition_history_page(
    user_id: str,
) -> requests.Response:
    url = f"{USERS_URL}/{user_id}/history"
    return requests.get(url)
