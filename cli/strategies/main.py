import click

from .create import create_strategies
from .delete import delete_strategies


@click.group(name="strategies", help="Strategies CLI")
def strategies_subcommands() -> None:
    pass


strategies_subcommands.add_command(create_strategies)
strategies_subcommands.add_command(delete_strategies)
