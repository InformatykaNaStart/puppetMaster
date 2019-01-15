import requests


class Api:
    base = 'https://api.packet.net/'
    token = None

    def __init__(self, token):
        self.token = token

    def call(self, method, endpoint, data = {}):
        resp = requests.request(method, self.base + endpoint, json=data, headers={'Content-Type': 'application/json', 'X-Auth-Token': self.token})
        if resp.status_code in [200, 201]:
            return resp.json()
        elif resp.status_code in [204]:
            return None
        else:
            raise Exception('%d %s' % (resp.status_code, resp.reason))

    def getPrices(self, facility, plan):
        resp = self.call('GET', 'plans')
        fullPrice = [i['pricing']['hour'] for i in resp['plans'] if i['slug'] == plan][0]

        resp = self.call('GET', 'market/spot/prices')
        curPrice = resp['spot_market_prices'][facility][plan]['price']

        return (fullPrice, curPrice)

