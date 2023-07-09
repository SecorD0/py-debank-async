from typing import Optional, Dict, List

from py_debank_async.models import Entrypoints, Chain
from py_debank_async.utils import get_proxy, check_response, async_get, get_headers


async def project_list(
        address: str, raw_data: bool = False, proxies: Optional[str or List[str]] = None
) -> Dict[str, Chain] or Dict[str, dict]:
    """
    Get projects where the account's assets are located (liquidity, staking, etc.)

    :param str address: the address
    :param bool raw_data: if True, it will return the unprocessed dictionary (False)
    :param Optional[str or List[str]] proxies: an HTTP proxy or a proxy list for random choice for making a request (None)
    :return Dict[str, Chain] or Dict[str, dict]: projects where the account's assets are located
    {
        'eth': Chain(..., projects=...),
        'bsc': Chain(..., projects=...)
    }
    """
    params = {
        'user_addr': address
    }
    status_code, json_response = await async_get(
        url=Entrypoints.PUBLIC.PORTFOLIO + 'project_list', params=params, headers=await get_headers(),
        proxy=await get_proxy(proxy=proxies)
    )
    await check_response(status_code=status_code, json_response=json_response)
    chain_dict = {}
    for token in json_response['data']:
        chain = token['chain']
        if chain in chain_dict:
            chain_dict[chain].append(token)

        else:
            chain_dict[chain] = [token]

    if not raw_data:
        chain_list = [Chain(name=name, projects=projects) for name, projects in chain_dict.items()]
        chain_dict = {}
        for chain in sorted(chain_list, key=lambda chain: chain.usd_value, reverse=True):
            chain_dict[chain.name] = chain

        chain_dict = {
            key: value for key, value in sorted(chain_dict.items(), key=lambda item: item[1].usd_value, reverse=True)
        }

    return chain_dict
