from typing import List, Dict
import json

from .alphavantage import AlphaVantageIntraDayExtend


class Spider():
    
    def __init__(self, config: Dict, *args, **kwargs) -> None:
        
        source = config['spider']['source']
        assert source in ['alphavantage'], f"Data source {source} is not found !"
        
        if len(config['spider']['symbols']):
            symbols_list = config['spider']['symbols']
        else:
            with open(config['spider']['default_symbol_list_path']) as f:
                symbols_list = json.safe_load(f)
            f.close()
            symbols_list = symbols_list['symbols']
        
        save_dir = config['spider']['save_dir']
    
        self.config = config
        self.source = config['spider']['source']
         
        match self.source:
            
            case 'alphavantage':
                self.spider = AlphaVantageIntraDayExtend(
                    symbols_list=symbols_list, 
                    interval=config['spider']['alphavantage']['interval'], 
                    slice=config['spider']['alphavantage']['slice'], 
                    adjusted=config['spider']['alphavantage']['adjusted'], 
                    api=config['spider']['alphavantage']['api']
                )
        
    def download(self) -> None:
        self.spider.download()
    
    def create_table(self) -> None:
        self.spider.create_table(database_path=self.config['spider']['save_dir'])