from atcoder.scrape.submission import (
    scrape_submission_summary,
    scrape_code,
    scrape_submission_id,
)


if __name__ == "__main__":
    from atcoder.crawl.submission import crawl_submission
    import asyncio

    async def test() -> None:
        response = await crawl_submission("abc236", 28755333)
        submission_summary = await scrape_submission_summary(response.content)
        print(submission_summary)
        print(await scrape_code(response.content))
        print(await scrape_submission_id(response.content))

    asyncio.run(test())
