import click

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.group()
@click.version_option()
def cli():
    pass

@cli.group(context_settings=CONTEXT_SETTINGS)
def spider():
    pass

@spider.command('run')
@click.option('--source',   '-s', type=str, required=True)
@click.option('--save_dir', '-d', type=str, required=True)
def run_spider(source, save_dir):
    print('Spider is running !')
    print(source)
    print(save_dir) 