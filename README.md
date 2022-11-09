# Momo Web Crawler

## Description

此專案可以指定關鍵字到 [Momo 行動版網頁](https://m.momoshop.com.tw) 去搜尋商品目錄、價格、以及產品編號。

## Installation

1. 需要先安裝 `Poetry` :

    `$ brew install poetry`

    也可以參考 [官方網站](https://python-poetry.org/docs/) 安裝方式進行安裝。

2. Clone 此 repo ：

    `$ git clone git@github.com:jack456054/momo_crawler.git`

3. 安裝 python 相依套件：

    `$ poetry install`

4. 執行 app ：

    `$ python3 main.py`

## APIs

Application 預設的位址是 http://127.0.0.1:5000/ 。

- GET `/items/` : 列出輸入 `keyword` 在 Momo 上面的商品資訊。
  
  - Request parameters:
  
    - `keyword`: 欲搜尋的商品關鍵字。

  - Response:
  
    - JSON 回傳格式：
  
    ```
    {
        "items": [ # 回傳值完整的商品資訊
            {
                "item_id": <string: 商品資訊>,
                "name": <string: 商品名稱>,
                "price": <string: 商品價格>
            },
            ...
        ],
        "error_items": [] # 缺少任意值的商品資訊
    }
    ```

    - HTTP Status Codes:
      - `200`: 全部商品資訊都齊全（排除重複）。
      - `204`: 無齊全資訊的商品。
      - `206`: 有部分商品資訊齊全，部分商品資訊不齊全。
      - `400`: Parameter 帶入錯誤。


## Tests

1. 執行測試：

    `poetry run pytest tests`

2. 因為本專案利用 `vcr` 去記錄外部 api 的結果， `mock` 去模擬 method 的回傳值，如果想要真的打外部 API 並且重新錄製 response ：
   
   `poetry run pytest tests --record-mode=rewrite`


## Examples

Request:

```
GET http://127.0.0.1:5000/items/?keyword=iphone14
```

Response: 

```
{
    "items": [
        {
            "item_id": "10525022",
            "name": "【Apple 蘋果】iPhone 14 128G(6.1吋)",
            "price": "26784"
        },
        {
            "item_id": "10525035",
            "name": "【Apple 蘋果】iPhone 14 Plus 128G(6.7吋)",
            "price": "29667"
        },
        ...
    ],
    "error_items": []
}
```
