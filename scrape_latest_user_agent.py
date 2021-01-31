#!/usr/bin/env python

from asyncio import run as asyncio_run
from typing import Type

from pyutils.argparse.typed_argument_parser import TypedArgumentParser
from httpx import AsyncClient

from scrape_latest_user_agent import Browser, OperatingSystem, scrape_latest_user_agent


class ScrapeLatestUserAgentArgumentParser(TypedArgumentParser):

    class Namespace:
        browser: str
        operating_system: str

    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            description='Obtain the latest user agent of a browser and operating system',
            epilog='The user agent is scraped from whatismybrowser.com.',
            **kwargs,
        )

        self.add_argument(
            'browser',
            help='The browser for which to obtain the latest user agent.',
            choices=[browser.value for browser in list(Browser)],
        )

        self.add_argument(
            '--operating-system',
            help='',
            choices=[operating_system.value for operating_system in list(OperatingSystem)],
            default='windows'
        )


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
