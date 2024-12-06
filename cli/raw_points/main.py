import click

from .create import create_raw_points


@click.group(name="raw_points", help="Raw Points CLI")
def raw_points_subcommands() -> None:
    pass


raw_points_subcommands.add_command(create_raw_points)
