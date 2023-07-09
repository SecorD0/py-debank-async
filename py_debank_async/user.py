from typing import Optional, List

from py_debank_async.models import Info, User, Entrypoints
from py_debank_async.utils import get_proxy, check_response, async_get, get_headers


async def addr(address: str, proxies: Optional[str or List[str]] = None) -> User:
    """
    Get a DeBank user.

    Args:
        address (str): an address.
        proxies (Optional[str or List[str]]): an HTTP proxy or a proxy list for random choice for making
            a request. (None)

    Returns:
        User: the DeBank user.

    """
    params = {
        'addr': address
    }
    status_code, json_response = await async_get(
        url=Entrypoints.PUBLIC.USER + 'addr', params=params, headers=await get_headers(),
        proxy=await get_proxy(proxy=proxies)
    )
    await check_response(status_code=status_code, json_response=json_response)
    return User(data=json_response['data'])


async def info(address: str, proxies: Optional[str or List[str]] = None) -> Info:
    """
    Get an information about a DeBank user.

    Args:
        address (str): an address.
        proxies (Optional[str or List[str]]): an HTTP proxy or a proxy list for random choice for making
            a request. (None)

    Returns:
        Info: the information about the DeBank user.

    """
    params = {
        'id': address
    }
    status_code, json_response = await async_get(
        url=Entrypoints.PUBLIC.ENTRYPOINT + 'hi/user/info', params=params, headers=await get_headers(),
        proxy=await get_proxy(proxy=proxies)
    )
    await check_response(status_code=status_code, json_response=json_response)
    return Info(data=json_response['data'])


async def total_balance(address: str, proxies: Optional[str or List[str]] = None) -> float:
    """
    Get a total balance of an address.

    Args:
        address (str): an address.
        proxies (Optional[str or List[str]]): an HTTP proxy or a proxy list for random choice for making
            a request. (None)

    Returns:
        float: the total balance.

    """
    params = {
        'addr': address
    }
    status_code, json_response = await async_get(
        url=Entrypoints.PUBLIC.USER + 'total_balance', params=params, headers=await get_headers(),
        proxy=await get_proxy(proxy=proxies)
    )
    await check_response(status_code=status_code, json_response=json_response)
    return json_response['data']['total_usd_value']
