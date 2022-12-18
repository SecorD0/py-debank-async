from typing import Optional, List

from py_debank_async.models import Entrypoints, Curve
from py_debank_async.utils import get_proxy, async_get, check_response, get_headers


async def net_curve_24h(address: str, proxies: Optional[str or List[str]] = None) -> Curve:
    """
    Get an address's asset value history for the last 24 hours.

    :param str address: the address
    :param Optional[str or List[str]] proxies: an HTTP proxy or a proxy list for random choice for making a request (None)
    :return Curve: the address's asset value history for the last 24 hours
    """
    params = {'user_addr': address}
    status_code, json_dict = await async_get(Entrypoints.PUBLIC.ASSET + 'net_curve_24h', params=params,
                                             headers=await get_headers(), proxy=await get_proxy(proxy=proxies))
    await check_response(status_code=status_code, json_dict=json_dict)
    return Curve(data=json_dict['data'])
