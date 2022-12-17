from typing import Optional, List

from fake_useragent import UserAgent

from py_debank_async.models import Info, User, Entrypoints
from py_debank_async.utils import get_proxy, check_response, async_get


async def addr(address: str, proxies: Optional[str or List[str]] = None) -> User:
    """
    Get a DeBank user.

    :param str address: an address
    :param Optional[str or List[str]] proxies: an HTTP proxy or a proxy list for random choice for making a request (None)
    :return User: the DeBank user
    """
    params = {'addr': address}
    headers = {'user-agent': UserAgent().chrome}
    proxy = await get_proxy(proxy=proxies)
    status_code, json_dict = await async_get(Entrypoints.PUBLIC.USER + 'addr', params=params, headers=headers,
                                             proxy=proxy)
    await check_response(status_code=status_code, json_dict=json_dict)
    return User(data=json_dict['data'])


async def info(address: str, proxies: Optional[str or List[str]] = None) -> Info:
    """
    Get an information about a DeBank user.

    :param str address: an address
    :param Optional[str or List[str]] proxies: an HTTP proxy or a proxy list for random choice for making a request (None)
    :return Info: the information about the DeBank user
    """
    params = {'id': address}
    headers = {'user-agent': UserAgent().chrome}
    proxy = await get_proxy(proxy=proxies)
    status_code, json_dict = await async_get(Entrypoints.PUBLIC.ENTRYPOINT + 'hi/user/info', params=params,
                                             headers=headers, proxy=proxy)
    await check_response(status_code=status_code, json_dict=json_dict)
    return Info(data=json_dict['data'])


async def total_balance(address: str, proxies: Optional[str or List[str]] = None) -> float:
    """
    Get a total balance of an address.

    :param str address: the address
    :param Optional[str or List[str]] proxies: an HTTP proxy or a proxy list for random choice for making a request (None)
    :return float: the total balance
    """
    params = {'addr': address}
    headers = {'user-agent': UserAgent().chrome}
    proxy = await get_proxy(proxy=proxies)
    status_code, json_dict = await async_get(Entrypoints.PUBLIC.USER + 'total_balance', params=params, headers=headers,
                                             proxy=proxy)
    await check_response(status_code=status_code, json_dict=json_dict)
    return json_dict['data']['total_usd_value']
