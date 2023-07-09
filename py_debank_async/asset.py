from typing import Optional, List

from py_debank_async.models import Entrypoints, Curve
from py_debank_async.utils import get_proxy, async_get, check_response, get_headers


async def net_curve_24h(address: str, proxies: Optional[str or List[str]] = None) -> Curve:
    """
    Get an address's asset value history for the last 24 hours.

    Args:
        address (str): an address.
        proxies (Optional[str or List[str]]): an HTTP proxy or a proxy list for random choice for making
            a request. (None)

    Returns:
        Curve: the address's asset value history for the last 24 hours.

    """
    params = {
        'user_addr': address
    }
    status_code, json_response = await async_get(
        url=Entrypoints.PUBLIC.ASSET + 'net_curve_24h', params=params, headers=await get_headers(),
        proxy=await get_proxy(proxy=proxies)
    )
    await check_response(status_code=status_code, json_response=json_response)
    return Curve(data=json_response['data'])
