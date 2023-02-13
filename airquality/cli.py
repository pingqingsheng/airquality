import os

import click
import yaml

from spider.spider import Spider
from __init__ import package_directory

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.group()
@click.version_option()
def cli():
    pass

@cli.group(context_settings=CONTEXT_SETTINGS)
def spider():
    pass

@spider.command('run')
@click.option('--source',   '-s', type=str)
@click.option('--save_dir', '-d', type=str)
def _run_spider(*args, **kwargs):
    
    with open(os.path.join(package_directory, 'default_config.yml')) as f:
        config = yaml.safe_load(f)
    f.close()
    config['spider'].update({k:v for k,v in kwargs.items() if v is not None})
    
    spider = Spider(config)
    spider.download()
    spider.create_table()
    