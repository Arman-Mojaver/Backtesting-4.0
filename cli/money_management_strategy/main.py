import click

from .create_multiple import create_multiple_money_management_strategies
from .delete_multiple import delete_multiple_money_management_strategies


@click.group(name="mm_strategies", help="Money Management Strategy CLI")
def money_management_strategies_subcommands() -> None:
    pass


money_management_strategies_subcommands.add_command(
    create_multiple_money_management_strategies
)
money_management_strategies_subcommands.add_command(
    delete_multiple_money_management_strategies
)
