import click

from .create import create_operation_points


@click.group(name="operation_points", help="Operation Points CLI")
def operation_points_subcommands() -> None:
    pass


operation_points_subcommands.add_command(create_operation_points)
