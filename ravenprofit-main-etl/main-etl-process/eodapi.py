from datetime import date
import os
from get_tickers import Get


CURRENT_DATE=date.today().strftime("%Y-%m-%d")
eodapi_KEY = os.getenv("EODAPI_KEY")



eodapi_exchanges = Get.get_eodapi_exchange(2)
eodapi_tickers = Get.get_eod_tickers(eodapi_exchanges[1], 2)


eodapi = []

for ticker in eodapi_tickers:
    eodapi.append( {
        "methods" : {
                      "get_json" : "Do.get_json",
                      "json_to_pandas" : "Do.json_to_pandas",
                      "save_to_parquet" : "Do.save_to_parquet"
                                   },
        "ticker" : ticker,
        "endpoint" : {  'dataprovider_name' : 'EODAPI',
                        'url' : f"https://eodhistoricaldata.com/api/eod/{ticker}.{eodapi_exchanges[1]}",
                                 'param' : {'from' : '2020-1-1',
                                            'to' : CURRENT_DATE,
                                            'filter' : 'last_close',
                                            "fmt" : "json",
                                            'period' : 'd',
                                            'api_token' : eodapi_KEY
                                            },
                                 'header' : None,
                                 }
    })
