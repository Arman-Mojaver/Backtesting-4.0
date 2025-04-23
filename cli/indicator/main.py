import click

from .delete_multiple import delete_multiple_indicators


@click.group(name="i", help="Indicator CLI")
def indicators_subcommands() -> None:
    pass


indicators_subcommands.add_command(delete_multiple_indicators)
