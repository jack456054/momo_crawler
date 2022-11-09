from time import sleep
from typing import Dict, List, Set

import requests
from bs4 import BeautifulSoup


def crawler(
    keyword: str,
    item_dict: List[Dict[str, str]],
    page: str = 1,
    _retry: int = 3,
    _id_set: Set[str] = None,
    _error_results: List[Dict[str, str]] = None,
) -> List[Dict[str, str]]:
    _id_set = _id_set or set()
    _error_results = _error_results or []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
    }
    url = (
        f'https://m.momoshop.com.tw/search.momo?searchKeyword={keyword}&curPage={page}'
    )
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    items = soup.find_all('li', class_='goodsItemLi')
    if _retry == 3:
        print(f'Fetching page {page} ...')
    if items:
        for i in items:
            item_id = i.find('input', id='viewProdId').get('value')
            name = i.find('h3', class_='prdName').text
            price = i.find('b', class_='price').text
            if not item_id or not name or not price:  # Exclude invalid items.
                _error_results.append(
                    {
                        'item_id': item_id,
                        'name': name,
                        'price': price,
                    }
                )
            else:
                if item_id not in _id_set:  # Avoid duplicate items.
                    item_dict.append(
                        {
                            'item_id': item_id,
                            'name': name,
                            'price': price,
                        }
                    )
            _id_set.add(item_id)
        return crawler(keyword, item_dict, page + 1, 3, _id_set, _error_results)
    else:
        if _retry > 0:
            sleep(2)
            return crawler(
                keyword, item_dict, page, _retry - 1, _id_set, _error_results
            )
        else:
            print(
                f'{len(item_dict)} items fetched.\n{len(_error_results)} invalid items fetched.'
            )
            return item_dict, _error_results
