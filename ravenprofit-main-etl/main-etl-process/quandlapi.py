from datetime import date
import os
from get_tickers import Get


CURRENT_DATE=date.today().strftime("%Y-%m-%d")
quandl_KEY = os.getenv("QUANDL_KEY")


quandl_METADATA = 'BATS_metadata.csv'



quandl_tickers = Get.get_tickers(quandl_METADATA, 10)


quandl=[]
for ticker in quandl_tickers:
    quandl.append( {
        "methods" : {
                      "get_json" : "Do.get_json",
                      "json_to_pandas_quandl" : "Do.json_to_pandas_quandl",
                      "save_to_parquet" : "Do.save_to_parquet"
                                   },
        "ticker" : ticker,
        "endpoint" : {'dataprovider_name' : 'QUANDLAPI',
                                 'url' : f"https://www.quandl.com/api/v3/datasets/BATS/{ticker}/data.json",
                                 'param' : {'startDate' : '2020-1-1',
                                            'endDate' : CURRENT_DATE,
                                            'api_key' : quandl_KEY,
                                            },
                                 'header' : {'Content-Type': 'application/json' },
                                 }
    })
