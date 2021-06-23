import click

from .core import Project

@click.command()
@click.option('-conf', '--config', 'config_path', help="Config File Path", required=True)
def run(config_path: str):
    # print(config_path)
    core = Project(config_path)