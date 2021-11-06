# Martins Klavins
# - by providing amount, currency and desired coin, get any price expressed in crypto
# - currency rates are gathered with JSON - provided from different API's

import requests


class Crypto:
    def __init__(self):
        self.connected = False
        self.currency = ""
        self.coin = ""
        self.rate = 0

    def get_price_in_crypto(self, in_price=0, in_currency="EUR", in_coin="BTC"):
        """
            validation:
            - validate two input parameters and connection to web pages
            - if error: returns error messages
            call API:
            - get data and store them in memory (so API called only on changed parameters)
            output:
            - return data (string) for user input
        """
        try:
            if self.currency != in_currency.upper() or self.coin != in_coin.upper():
                if not self.connected:
                    self.connected = self.validate_api()
                self.currency = self.validate_currency(in_currency)
                self.coin = self.validate_coin(in_coin)
                self.call_api()

            return str(float(in_price) * self.rate) + " " + self.coin
        except Exception as error:
            return "error: " + str(error)

    @staticmethod
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

    @staticmethod
    def validate_coin(in_coin):
        edited_coin = in_coin.upper()
        response = requests.get('https://api.coinpaprika.com/v1/coins')
        for element in response.json():
            if (element.get("id").upper()).find(edited_coin) >= 0:
                return element.get("symbol")
        raise ValueError("invalid coin name!")

    @staticmethod
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

    def call_api(self):
        response = requests.get(f'https://api.coindesk.com/v1/bpi/currentprice/{self.currency}.json')
        data = response.json()
        btc = (data.get("bpi")).get(self.currency)
        btc_rate = 1/btc.get("rate_float")

        if self.coin != "BTC":
            response = requests.get(f'https://api.binance.com/api/v3/ticker/price?symbol={self.coin}BTC')
            data = response.json()
            self.rate = (1 / float(data.get("price"))) * btc_rate
        else:
            self.rate = btc_rate


if __name__ == '__main__':
    example = Crypto()
    print(example.get_price_in_crypto(4500, "usd", "ETH"))
    print(example.get_price_in_crypto(400, "usd", "ETH"))
    print(example.get_price_in_crypto(4500, "usd", "+"))
