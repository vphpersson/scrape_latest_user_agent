#!/usr/bin/env python

from asyncio import run as asyncio_run
from typing import Type

from httpx import AsyncClient

from scrape_latest_user_agent import Browser, OperatingSystem, scrape_latest_user_agent
from scrape_latest_user_agent.cli import ScrapeLatestUserAgentArgumentParser


async def main():
    args: Type[ScrapeLatestUserAgentArgumentParser.Namespace] = ScrapeLatestUserAgentArgumentParser().parse_args()

    async with AsyncClient() as http_client:
        print(
            await scrape_latest_user_agent(
                browser=Browser(args.browser),
                operating_system=OperatingSystem(args.operating_system),
                http_client=http_client
            )
        )


if __name__ == '__main__':
    asyncio_run(main())
