from datetime import date
import os
from get_tickers import Get


CURRENT_DATE=date.today().strftime("%Y-%m-%d")
eodapi_KEY = os.getenv("EODAPI_KEY")



eodapi_exchanges = Get.get_eodapi_exchange(1)
eodapi_tickers = Get.get_eod_tickers(eodapi_exchanges[0], 1)



eodapi_endpoints = []
for ticker in eodapi_tickers:
    eodapi_endpoints.append({'url' : f"https://eodhistoricaldata.com/api/eod/{ticker}.{eodapi_exchanges[4]}",
                             'param' : {'from' : '2020-1-1',
                                        'to' : CURRENT_DATE,
                                        'filter' : 'last_close',
                                        'period' : 'd',
                                        'token' : eodapi_KEY
                                        },
                             'header' : None,
                             })

eod = {'endpoints' : eodapi_endpoints,
       'tickers' : eodapi_tickers,
      }
