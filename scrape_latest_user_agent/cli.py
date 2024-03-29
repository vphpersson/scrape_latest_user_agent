from typed_argument_parser import TypedArgumentParser

from scrape_latest_user_agent import Browser, OperatingSystem


class ScrapeLatestUserAgentArgumentParser(TypedArgumentParser):

    class Namespace:
        browser: str
        operating_system: str

    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            **(
                dict(
                    description='Obtain the latest user agent of a browser and operating system',
                    epilog='The user agent is scraped from whatismybrowser.com.',
                ) | kwargs
            )
        )

        self.add_argument(
            'browser',
            help='The browser for which to obtain the latest user agent.',
            choices=[browser.value for browser in list(Browser)],
        )

        self.add_argument(
            '--operating-system',
            help='The operating system for which to obtain the latest user agent.',
            choices=[operating_system.value for operating_system in list(OperatingSystem)],
            default='windows'
        )
