import requests

connected = False
currency = ""
coin = ""
rate = 0


def get_price_in_crypto(in_price=0, in_currency="EUR", in_coin="BTC"):
    global connected
    global currency
    global rate
    global coin

    """
    validation:
    - validate two input parameters and connection to web pages
    - returns error codes/messages
    call API:
    - get data and store them in memory
    output:
    - return data for user input
    """
    try:
        if currency != in_currency.upper() or coin != in_coin.upper():
            if not connected:
                connected = validate_api()
            currency = validate_currency(in_currency)
            coin = validate_coin(in_coin)
            call_api()
        return str(float(in_price) * rate) + " " + coin

    except Exception as error:
        return "error: " + str(error)


def validate_currency(in_currency):
    edited_currency = in_currency.upper()
    response = requests.get('https://api.coindesk.com/v1/bpi/supported-currencies.json')
    for element in response.json():
        if element.get("currency") == edited_currency:
            return edited_currency
    for element in response.json():
        if (element.get("country").upper()).find(edited_currency) >= 0:
            return element.get("currency")
    raise ValueError("invalid currency name!")


def validate_coin(in_coin):
    edited_coin = in_coin.upper()
    response = requests.get('https://api.coinpaprika.com/v1/coins')
    for element in response.json():
        if (element.get("id").upper()).find(edited_coin) >= 0:
            return element.get("symbol")
    raise ValueError("invalid coin name!")


def validate_api():
    # https://realpython.com/python-requests/ + get(url, timeout=3)
    for url in ['https://api.coindesk.com', 'https://api.binance.com', 'https://api.coinpaprika.com']:
        response = requests.get(url)
        # 'response' will evaluate to True if the status code was between 200 and 400, and False otherwise.
        if response:
            connection = True
        else:
            # this code will be unreached anyway if requests.get raise exception, I leave if for readability
            connection = False
    return connection


def call_api():
    global rate
    response = requests.get(f'https://api.coindesk.com/v1/bpi/currentprice/{currency}.json')
    data = response.json()
    btc = (data.get("bpi")).get(currency)
    btc_rate = 1/btc.get("rate_float")

    if coin != "BTC":
        response = requests.get(f'https://api.binance.com/api/v3/ticker/price?symbol={coin}BTC')
        data = response.json()
        rate = (1 / float(data.get("price"))) * btc_rate
    else:
        rate = btc_rate


if __name__ == '__main__':
    print(get_price_in_crypto(4480, "usd", "ether"))
    print(get_price_in_crypto(4500, "usd", "ETH"))
    print(get_price_in_crypto(500, "usd", "+"))
