import os
from typing import List
from itertools import product
import re

import csv
import requests
import pandas as pd
import numpy as np
import json

class AlphaVantageIntraDayExtend():
    
    def __init__(self, 
                 symbols_list: List, 
                 interval: str, 
                 slice: str, 
                 adjusted: bool = True, 
                 api: str = 'demo') -> None:
        
        assert interval in ('1min', '5min', '15min', '30min', '60min'), f'Interval {interval} is not supported !'
        assert slice in (f'year{ym[0]:d}month{ym[1]:d}' for ym in product(range(1,3), range(1, 13))), f'Slice {slice} is not supported !'
        
        self.symbols_list = symbols_list
        self.interval = interval
        self.slice  = slice 
        self.adjust = adjusted
        
        self._api = api
        
        self.api_url_list = []
        for symbol in self.symbols_list:
            _api =  f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY_EXTENDED&symbol={symbol}&adjusted={self.adjust}&interval={self.interval}&slice={self.slice}&apikey={self._api}'
            self.api_url_list.append(_api)
        
            
    def download(self) -> None:
        
        self.df = {}
        
        with requests.Session() as s:
            
            for _api in self.api_url_list: 
                
                download = s.get(_api)
                decoded_content = download.content.decode('utf-8')
                cr = list(csv.reader(decoded_content.splitlines(), delimiter=','))
                symbol_dict = {x[0]:list(x[1:]) for x in zip(*cr)}
                
                symbol = re.findall(re.compile('.*symbol=([a-zA-Z]+)&.*'), _api)[0]
                self.df[symbol] = symbol_dict
    
    
    def create_table(self, database_path: str) -> None:
        
        os.makedirs(os.path.join(database_path, 'alpha_vantage'), exist_ok=True)
        
        for k in self.df:
            
            table_name = f"{k}_{self.interval}_{self.slice}.json"
            
            with open(os.path.join(database_path, table_name), 'w') as f: 
                json.dump(self.df[k], f, sort_keys=True, indent=4)
            f.close()