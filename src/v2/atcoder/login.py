from atcoder.constant import _SITE_URL

LOGIN_URL = f"{_SITE_URL}/login"


from atcoder.core.crawl.constant import LOGIN_URL


# async def get_login_page(
#     session: typing.Optional[requests.Session] = None,
# ) -> requests.models.Response:
#     if session is None:
#         return requests.get(LOGIN_URL)
#     return session.get(LOGIN_URL)


# @dataclasses.dataclass
# class _LoginPostParams:
#     username: str
#     password: str
#     csrf_token: str


# async def post_login(
#     session: requests.Session,
#     post_params: _LoginPostParams,
# ) -> requests.models.Response:
#     return session.post(
#         url=LOGIN_URL,
#         data=dataclasses.asdict(post_params),
#     )


# async def scrape_csrf_token(html: bytes) -> str:
#     soup = _parse_html(html)
#     return unwrap(await scrape_csrf_token_in_form(soup.find_all("form")[1]))
