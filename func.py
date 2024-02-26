import requests
import pandas as pd

def get_info():
    response = requests.get(url="https://yobit.net/api/3/info")
    with open ("info.txt", "w") as f:
        f.write(response.text)
    return response.text 

def get_ticker(wallet1,wallet2):
    response = requests.get(url=f"https://yobit.net/api/3/ticker/{wallet1}_{wallet2}?ignore_invalid=1")
    with open("tikcers.txt","w") as f:
        f.write(response.text)
    return response.text

def get_depth(wallet1,wallet2,limit=150):
    response = requests.get(url=f"https://yobit.net/api/3/depth/{wallet1}_{wallet2}?limit={limit}?ignore_invalid=1")
    with open("depth.txt","w") as f:
        f.write(response.text)

    bids = response.json()[f"{wallet1}_usdt"]["bids"]
    total_bids_amount=0
    for item in bids:
        price = item[0]
        wallet_weight = item[1]
        total_bids_amount += price * wallet_weight
    return f"{total_bids_amount} $$$"


def get_trades(wallet1, wallet2, limit=150):  
    response = requests.get(url=f"https://yobit.net/api/3/trades/{wallet1}_{wallet2}?limit={limit}")
    total_trade_asks = 0
    total_trade_bids = 0
    for item in response.json()[f"{wallet1}_{wallet2}"]:
        if item["type"] == "ask":
            total_trade_asks += item["price"] * item["amount"]
        else:
            total_trade_bids += item["price"] * item["amount"]
    return f"{wallet1.upper()}/{wallet2.upper()} TOTAL SELL {round(total_trade_asks, 2)} $$$\n{wallet1.upper()}/{wallet2.upper()} TOTAL BUY {round(total_trade_bids, 2)} $$$"

def data_framed(wallet1, wallet2, limit=150):
    response = requests.get(url=f"https://yobit.net/api/3/trades/{wallet1}_{wallet2}?limit={limit}")
    df = pd.json_normalize(response.json()[f"{wallet1}_{wallet2}"])
    df.drop(columns=['tid', 'timestamp'], inplace=True)
    df.rename(columns={'amount': 'Количество', 'price': 'Цена', 'type': 'Тип'}, inplace=True)
    df['Тип'] = df['Тип'].map({'ask': 'Покупка', 'bid': 'Продажа'})
    df['Цена'] = df['Цена'].round(2)
    return df.head(11).to_string(index=False)
