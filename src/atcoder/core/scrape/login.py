from atcoder.core.scrape.form import scrape_csrf_token_in_form
from atcoder.core.scrape.utils import parse_html
from atcoder.core.utils import unwrap


async def scrape_csrf_token(html: bytes) -> str:
    soup = await parse_html(html)
    return unwrap(await scrape_csrf_token_in_form(soup.find_all("form")[1]))
