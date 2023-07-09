import random
from typing import Optional, List, Tuple

import aiohttp
from fake_useragent import UserAgent

from py_debank_async import exceptions


async def get_headers() -> dict:
    """
    Get headers for a request.

    :return dict: headers
    """
    return {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'origin': 'https://debank.com',
        'referer': 'https://debank.com/',
        'source': 'web',
        'user-agent': UserAgent().chrome
    }


async def get_proxy(proxy: Optional[str or List[str]] = None) -> Optional[str]:
    """
    Choose a proxy for a request.

    :param Optional[str or List[str]] proxy: an HTTP proxy or a proxy list for random choice for making a request (None)
    :return Optional[dict]: the proxy dictionary with the selected proxy
    """
    if not proxy:
        return

    if isinstance(proxy, str):
        proxy = proxy

    elif isinstance(proxy, list):
        proxy = random.choice(proxy)

    else:
        return

    if 'http' not in proxy:
        proxy = f'http://{proxy}'

    return proxy


async def check_response(status_code: int, json_response: dict) -> None:
    """
    Check if a request was sent successfully.

    :param int status_code: the request status code
    :param dict json_response: a JSON dictionary retrieved from the request
    """
    if status_code != 200:
        raise exceptions.DebankException(status_code=status_code)

    if json_response['error_code']:
        raise exceptions.DebankException(status_code=status_code, error_msg=json_response['error_msg'])


async def async_get(url: str, params: dict, headers: dict, proxy: str) -> Tuple[int, dict]:
    """
    Make asynchronous GET request.

    :param str url: a URL
    :param dict params: params for the request
    :param dict headers: headers for the request
    :param str proxy: an HTTP proxy in the format: http://user:password@ip:port
    :return Tuple[int, dict]: a status code of the request and a parsed JSON dictionary
    """
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url, params=params, proxy=proxy) as response:
            status = response.status
            if status == 200:
                json_response = await response.json()

            else:
                json_response = {}

            return status, json_response
