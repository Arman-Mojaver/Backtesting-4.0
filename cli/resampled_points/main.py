import click

from .create import create_resampled_points
from .delete import delete_resampled_points


@click.group(name="resampled_points", help="Resampled Points CLI")
def resampled_points_subcommands() -> None:
    pass


resampled_points_subcommands.add_command(create_resampled_points)
resampled_points_subcommands.add_command(delete_resampled_points)
