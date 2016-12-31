import time
import sys

from okcoincnapi.OkcoinSpotAPI import OKCoinSpot


def api_query(qfunc, opts=(), timelim=600, timeincr=5):
    res = None
    count = 0
    while res is None and count < timelim:
        try:
            res = qfunc(*opts)
            return res
        except:
            print(time.strftime("%d/%m/%Y %H:%M:%S"), 'Internal Error')

        count += timeincr
        time.sleep(timeincr)
        res = None

    sys.exit("Process aborded")


class OKCoincnInterfaceReal:
    def __init__(self, keyfile):
        resturl, apikey, secretkey = open(keyfile).read().splitlines()
        self.okcoinspot = OKCoinSpot(resturl, apikey, secretkey)

        self.gettrades = lambda tsince=0: api_query(self.okcoinspot.trades, ('btc_cny', tsince))
        self.getdepth = lambda n=10: api_query(self.okcoinspot.depth, ('btc_cny', n))
        self.getbalance = lambda: api_query(self.okcoinspot.userinfo)


if __name__ == '__main__':
    import json

    with open('../paramstraders.json') as params_file:
        params_trader_okcoincn = json.load(params_file)['okcoincn']

    apiokcoincn = OKCoincnInterfaceReal('../'+params_trader_okcoincn['keyfile'])

    print(apiokcoincn.getbalance())
    print(apiokcoincn.gettrades(0))
    print(apiokcoincn.getdepth(5))
