from typing import Optional, List, Dict

from fake_useragent import UserAgent

from py_debank_async.models import Entrypoints, Chain, ChainNames
from py_debank_async.utils import get_proxy, check_response, async_get


async def balance_list(address: str, chain: ChainNames or str, raw_data: bool = False,
                       proxies: Optional[str or List[str]] = None) -> Chain or dict:
    """
    Get token balances of an address of a certain chain.

    :param str address: the address
    :param ChainNames or st chain: the chain
    :param bool raw_data: if True, it will return the unprocessed dictionary (False)
    :param Optional[str or List[str]] proxies: an HTTP proxy or a proxy list for random choice for making a request (None)
    :return Chain: token balances
    """
    params = {'user_addr': address, 'is_all': 'false', 'chain': chain}
    headers = {'user-agent': UserAgent().chrome}
    proxy = await get_proxy(proxy=proxies)
    status_code, json_dict = await async_get(Entrypoints.PUBLIC.TOKEN + 'balance_list', params=params, headers=headers,
                                             proxy=proxy)
    await check_response(status_code=status_code, json_dict=json_dict)
    if raw_data:
        return {chain: json_dict['data']}

    return Chain(name=chain, tokens=json_dict['data'])


async def cache_balance_list(address: str, raw_data: bool = False,
                             proxies: Optional[str or List[str]] = None) -> Dict[str, Chain] or Dict[str, dict]:
    """
    Get token balances of an address of all chains.

    :param str address: the address
    :param bool raw_data: if True, it will return the unprocessed dictionary (False)
    :param Optional[str or List[str]] proxies: an HTTP proxy or a proxy list for random choice for making a request (None)
    :return Dict[str, Chain] or Dict[str, dict]: token balances
    {
        'eth': Chain(..., tokens=...),
        'bsc': Chain(..., tokens=...)
    }
    """
    params = {'user_addr': address}
    headers = {'user-agent': UserAgent().chrome}
    proxy = await get_proxy(proxy=proxies)
    status_code, json_dict = await async_get(Entrypoints.PUBLIC.TOKEN + 'cache_balance_list', params=params,
                                             headers=headers, proxy=proxy)
    await check_response(status_code=status_code, json_dict=json_dict)
    chain_dict = {}
    for token in json_dict['data']:
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
