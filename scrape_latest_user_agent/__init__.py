from logging import getLogger
from typing import Optional, Pattern
from collections import defaultdict
from enum import Enum
from html.parser import HTMLParser
from re import compile as re_compile

from httpx import AsyncClient, Response

LOG = getLogger(__name__)


class Browser(Enum):
    CHROME = 'chrome'
    FIREFOX = 'firefox'


class OperatingSystem(Enum):
    WINDOWS = 'windows'
    MAC_OS = 'mac_os'
    LINUX = 'linux'


class _WhatIsMyBrowserHTMLParser(HTMLParser):

    H2_OPERATING_SYSTEM_PATTERN: Pattern = re_compile(pattern=r'^Latest .+ on (?P<operating_system>.+) User Agents$')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._last_encountered_operating_system: Optional[str] = None
        self._operating_system_to_user_agents: dict[str, list[str]] = defaultdict(list)

        self._latest_tag: Optional[str] = None
        self._next_is_user_agent_element: bool = False

    @staticmethod
    def _attr_to_dict(attrs_list: list[tuple[str, str]]) -> dict[str, str]:
        return {key: value for key, value in attrs_list}

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str]]) -> None:
        self._latest_tag = tag
        self._next_is_user_agent_element = tag == 'span' and self._attr_to_dict(attrs_list=attrs).get('class') == 'code'

    def handle_data(self, data: str) -> None:
        if self._latest_tag == 'h2':
            if match := self.H2_OPERATING_SYSTEM_PATTERN.match(string=data):
                self._last_encountered_operating_system = match.groupdict()['operating_system']
                return
        elif self._next_is_user_agent_element:
            if trimmed_data := data.strip():
                self._operating_system_to_user_agents[self._last_encountered_operating_system].append(trimmed_data)

    @classmethod
    def parse(cls, html_content: str) -> dict[str, list[str]]:
        parser = cls()
        parser.feed(data=html_content)

        return parser._operating_system_to_user_agents

    def error(self, message: str) -> None:
        LOG.error(message)


async def scrape_latest_user_agent(
    browser: Browser,
    operating_system: OperatingSystem,
    http_client: AsyncClient
) -> Optional[str]:
    """
    Obtain the latest user agent for a specified browser and operating system.

    The user agent is scraped from whatismybrowser.com

    :param browser: The browser of the user agent to obtain.
    :param operating_system: The operating system of the user agent to obtain.
    :param http_client: An HTTP client with which to retrieve the HTML page which to scrape from.
    :return: The user agent corresponding to the provided arguments.
    """

    response: Response = await http_client.get(
        url=f'https://www.whatismybrowser.com/guides/the-latest-user-agent/{browser.value}'
    )
    response.raise_for_status()

    operating_system_to_user_agent_list: dict[str, list[str]] = _WhatIsMyBrowserHTMLParser.parse(
        html_content=response.text
    )

    if browser is Browser.CHROME:
        if operating_system is OperatingSystem.WINDOWS:
            label = 'Windows'
        elif operating_system is OperatingSystem.MAC_OS:
            label = 'macOS'
        elif operating_system is OperatingSystem.LINUX:
            label = 'Linux'
        else:
            label = None

        return (
            next(iter(user_agent_list), None)
            if (user_agent_list := operating_system_to_user_agent_list.get(label))
            else None
        )
    elif browser is Browser.FIREFOX:
        if operating_system is OperatingSystem.WINDOWS:
            index = 0
        elif operating_system is OperatingSystem.MAC_OS:
            index = 1
        elif operating_system is OperatingSystem.LINUX:
            index = 2
        else:
            index = None

        return (
            operating_system_to_user_agent_list['Desktop'][index]
            if index is not None
            else None
        )
    else:
        return None
