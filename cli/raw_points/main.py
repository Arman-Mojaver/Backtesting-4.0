import click

from .create import create_raw_points
from .delete import delete_raw_points


@click.group(name="r", help="Raw Point CLI")
def raw_points_subcommands() -> None:
    pass


raw_points_subcommands.add_command(create_raw_points)
raw_points_subcommands.add_command(delete_raw_points)
