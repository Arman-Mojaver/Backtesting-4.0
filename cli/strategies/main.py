import click

from .create import create_strategies


@click.group(name="strategies", help="Strategies CLI")
def strategies_subcommands() -> None:
    pass


strategies_subcommands.add_command(create_strategies)
