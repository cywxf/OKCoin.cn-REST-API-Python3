import time
import sys

from okcoincnapi.OkcoinSpotAPI import OKCoinSpot


def api_query(qfunc, opts=(), timelim=600, timeincr=5):
    res = []
    count = 0
    while not res and count < timelim:
        try:
            res = qfunc(*opts)
            if isinstance(res, dict):
                if 'error_code' in res.keys():
                    print(time.strftime("%d/%m/%Y %H:%M:%S"), 'API Error :', res['error_code'])
                else:
                    return res
            else:
                return res

        except:
            print(time.strftime("%d/%m/%Y %H:%M:%S"), 'Internal Error')

        count += timeincr
        time.sleep(timeincr)
        res = []

    sys.exit("Process aborded")


class OKCoincnInterface:
    def __init__(self, keyfile):
        resturl, apikey, secretkey = open(keyfile).read().splitlines()
        self.okcoinspot = OKCoinSpot(resturl, apikey, secretkey)

        self.gettrades = lambda tsince=0: api_query(self.okcoinspot.trades, ('btc_cny', tsince))
        self.getdepth = lambda n=10: api_query(self.okcoinspot.depth, ('btc_cny', n))
        self.getbalance = lambda: api_query(self.okcoinspot.userinfo)


if __name__ == '__main__':

    apiokcoincn = OKCoincnInterface("okcoincnapi.keys")

    print(apiokcoincn.getbalance())
    print(apiokcoincn.gettrades(0))
    print(apiokcoincn.getdepth(10))
