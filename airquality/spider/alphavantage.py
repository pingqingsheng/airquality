import os
from typing import List
from itertools import product
import re

import csv
import requests
import pandas as pd
import numpy as np
import json
from tqdm import tqdm

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
            
            for _api in (pbar := tqdm(self.api_url_list, ncols=100)): 
                
                download = s.get(_api)
                decoded_content = download.content.decode('utf-8')
                cr = list(csv.reader(decoded_content.splitlines(), delimiter=','))
                symbol_dict = {x[0]:list(x[1:]) for x in zip(*cr)}
                
                find_symbol = re.findall(re.compile('.*symbol=([a-zA-Z]+)&.*'), _api)
                if len(find_symbol):
                    symbol = find_symbol[0]
                    self.df[symbol] = symbol_dict
                    pbar.set_description(f"{symbol}")
    
    def create_table(self, database_path: str) -> None:
        
        source_dir = os.path.join(database_path, 'alphavantage')
        os.makedirs(source_dir, exist_ok=True)
        
        for k in self.df:
            
            asset_dir = os.path.join(source_dir, k, self.interval)
            os.makedirs(asset_dir, exist_ok=True)
            
            table_name = f"{self.slice}.json"
            
            with open(os.path.join(asset_dir, table_name), 'w') as f: 
                json.dump(self.df[k], f, sort_keys=True, indent=4)
            f.close()