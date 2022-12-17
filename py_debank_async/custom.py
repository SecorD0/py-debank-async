from typing import Dict, Optional, List

from py_debank_async.models import Chain, ChainNames
from py_debank_async import nft
from py_debank_async import portfolio
from py_debank_async import token


async def get_balance(address: str, chain: ChainNames or str = '',
                      proxies: Optional[str or List[str]] = None) -> Dict[str, Chain]:
    """
    Get the following information of an address of one or all chains:
    - token balances
    - projects where the account's assets are located
    - owned NFTs

    :param str address: the address
    :param ChainNames or st chain: the chain (all chains)
    :param Optional[str or List[str]] proxies: an HTTP proxy or a proxy list for random choice for making a request (None)
    :return Chain: the address information
    """
    chains: Dict[str, Chain] = {}
    if chain:
        nfts = await nft.collection_list(address=address, chain=chain, proxies=proxies)
        chains.update(nfts)

        tokens = await token.balance_list(address=address, chain=chain, raw_data=True, proxies=proxies)
        if tokens:
            chains[chain].parse_tokens(tokens[chain])

        projects = await portfolio.project_list(address=address, raw_data=True, proxies=proxies)
        if chain in projects:
            chains[chain].parse_projects(projects[chain])

    else:
        nfts = await nft.collection_list(address=address, proxies=proxies)
        chains.update(nfts)

        tokens = await token.cache_balance_list(address=address, raw_data=True, proxies=proxies)
        for name, token_dict in tokens.items():
            if name in chains:
                chains[name].parse_tokens(token_dict)

            else:
                chains[name] = Chain(name=name, tokens=token_dict)

        projects = await portfolio.project_list(address=address, raw_data=True, proxies=proxies)
        for name, project_dict in projects.items():
            if name in chains:
                chains[name].parse_projects(project_dict)

            else:
                chains[name] = Chain(name=name, projects=project_dict)

    chains = {key: value for key, value in sorted(chains.items(), key=lambda item: item[1].usd_value, reverse=True)}
    return chains