from typing import Optional, List, Dict

from py_debank_async.models import Entrypoints, Chain, ChainNames
from py_debank_async.utils import get_proxy, check_response, async_get, get_headers


async def balance_list(
        address: str, chain: ChainNames or str, raw_data: bool = False, proxies: Optional[str or List[str]] = None
) -> Chain or dict:
    """
    Get token balances of an address of a certain chain.

    :param str address: the address
    :param ChainNames or str chain: the chain
    :param bool raw_data: if True, it will return the unprocessed dictionary (False)
    :param Optional[str or List[str]] proxies: an HTTP proxy or a proxy list for random choice for making a request (None)
    :return Chain: token balances
    """
    params = {
        'user_addr': address,
        'is_all': 'false',
        'chain': chain
    }
    status_code, json_response = await async_get(
        url=Entrypoints.PUBLIC.TOKEN + 'balance_list', params=params, headers=await get_headers(),
        proxy=await get_proxy(proxy=proxies)
    )
    await check_response(status_code=status_code, json_response=json_response)
    if raw_data:
        return {chain: json_response['data']}

    return Chain(name=chain, tokens=json_response['data'])


async def cache_balance_list(
        address: str, raw_data: bool = False, proxies: Optional[str or List[str]] = None
) -> Dict[str, Chain] or Dict[str, dict]:
    """
    Get cached token balances of an address of all chains (current at the time of the last balance_list queries).

    :param str address: the address
    :param bool raw_data: if True, it will return the unprocessed dictionary (False)
    :param Optional[str or List[str]] proxies: an HTTP proxy or a proxy list for random choice for making a request (None)
    :return Dict[str, Chain] or Dict[str, dict]: token balances
    {
        'eth': Chain(..., tokens=...),
        'bsc': Chain(..., tokens=...)
    }
    """
    params = {
        'user_addr': address
    }
    status_code, json_response = await async_get(
        url=Entrypoints.PUBLIC.TOKEN + 'cache_balance_list', params=params, headers=await get_headers(),
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
        chain_list = [Chain(name=name, tokens=tokens) for name, tokens in chain_dict.items()]
        chain_dict = {}
        for chain in sorted(chain_list, key=lambda chain: chain.usd_value, reverse=True):
            chain_dict[chain.name] = chain

    return chain_dict
