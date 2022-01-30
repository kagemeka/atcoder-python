# import asyncio
# import typing

# import bs4
# import requests

# from atcoder.crawl.submission import crawl_submission
# from atcoder.crawl.submissions import RequestParams, crawl_submissions_page
# from atcoder.crawl.utils import fetch_page_source
# from atcoder.scrape.utils import parse_html


# async def submissions() -> None:
#     params = RequestParams(user="Kagemeka")
#     response = await crawl_submissions_page("abc236", params, page_id=0)
#     soup = await parse_html(response.content)
#     for data in soup.table.tbody.find_all("tr"):
#         # print(data.prettify())
#         # print()
#         ...


# async def submission() -> None:
#     response = await crawl_submission("abc236", 28755333)
#     soup = await parse_html(response.content)
#     print(soup.prettify())


# async def main() -> None:
#     await submissions()
#     await submission()


# if __name__ == "__main__":
#     asyncio.run(main())
