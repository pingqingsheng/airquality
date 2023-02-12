from typing import List, Dict
import json

from alphavantage import AlphaVantageIntraDayExtend


class Spider():
    
    def __init__(self, config: Dict, *args, **kwargs) -> None:
        
        source = config['spider']['source']
        assert source in ['alphavantage'], f"Data source {source} is not found !"
        
        if config['spider']['symbol']:
            symbols_list = config['spider']['symbol']
        else:
            with open(config['spider']['default_symbol_list_path']) as f:
                symbols_list = json.safe_load(f)
            f.close()
            symbols_list = symbols_list['symbols']
        
        save_dir = config['spider']['save_dir']
    
        self.config = config
         
        match self.source:
            
            case 'alphavantage':
                self.spider = AlphaVantageIntraDayExtend(
                    symbols_list=symbols_list, 
                    interval=config['crawler']['alpha_vantage']['interval'], 
                    slice=config['crawler']['alpha_vantage']['slice'], 
                    adjusted=config['crawler']['alpha_vantage']['adjusted'], 
                    api=config['crawler']['alpha_vantage']['api']
                )
        
    def download(self) -> None:
        self.spider.download()
    
    def create_table(self) -> None:
        self.crawler.create_table(database_path=self.config['crawler']['alpha_vantage']['database_path'])