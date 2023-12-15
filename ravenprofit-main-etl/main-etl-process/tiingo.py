from datetime import date
import os
from get_tickers import Get
CURRENT_DATE=date.today().strftime("%Y-%m-%d")


tiingo_KEY = os.getenv("TIINGO_KEY")
tiingo_METADATA = 'supported_tickers.csv'





selected_exchanges= ['PINK','NASDAQ']
filtered_tiingo_tickers = Get.get_filtered_tickers(tiingo_METADATA, selected_exchanges, 10)

#print(filtered_tiingo_tickers)

tiingo = []

for ticker in filtered_tiingo_tickers:
    tiingo.append( {
        "methods" : {
                      "get_json" : "Do.get_json",
                      "json_to_pandas" : "Do.json_to_pandas",
                      "save_to_parquet" : "Do.save_to_parquet"
                                   },
        "ticker" : ticker,
        "endpoint" : {'dataprovider_name' : 'TIINGOAPI',
                                 'url' : f"https://api.tiingo.com/tiingo/daily/{ticker}/prices",
                                 'param' : {'startDate' : '2020-1-1',
                                            'endDate' : CURRENT_DATE,
                                            'fromat' : 'json',
                                            'resampleFreq' : 'daily',
                                            'token' : tiingo_KEY,
                                            },
                                 'header' : {'Content-Type': 'application/json' },
                                 }
    })





#tiingo = {'endpoints' : tiingo_endpoints,
#          'tickers' : filtered_tiingo_tickers,
#         }
