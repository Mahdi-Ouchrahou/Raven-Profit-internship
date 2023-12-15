from datetime import date
import os
from get_tickers import Get

CURRENT_DATE=date.today().strftime("%Y-%m-%d")
iexcloud_KEY = os.getenv("IEXCLOUD_KEY")


iexcloud_exchanges = ["TSE",
                "LON",
                "KRX",
                "MEX",
                "BOM",
                "TSX",
                "TAE",
                "PAR",
                "ETR",
                "AMS",
                "BRU",
                "DUB",
                "LIS",
                "ADS"]

iexcloud_tickers = Get.get_iexcloud_ticker(iexcloud_exchanges[8],3)


iexcloud_endpoints = []
range = 5

iexcloud=[]
for ticker in iexcloud_tickers:
    iexcloud.append( {
        "methods" : {
                      "get_json" : "Do.get_json",
                      "json_to_pandas" : "Do.json_to_pandas",
                      "save_to_parquet" : "Do.save_to_parquet"
                                   },
        "ticker" : ticker,
        "endpoint" : {'dataprovider_name' : 'IEXCLOUD',
                                   'url' : f"https://cloud.iexapis.com/stable/stock/{ticker}/chart/{range}",
                                   'param' : {
                                            'chartCloseOnly' : True,
                                            'token' : iexcloud_KEY,
                                            },
                                   'header' : None,
                                 }
    })
