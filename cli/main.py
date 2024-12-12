import sys
from pathlib import Path

import click

sys.path.append(Path(__file__).resolve().parent.parent.as_posix())


from .money_management_strategy.main import money_management_strategies_subcommands
from .pytest.pytest_one import run_test
from .raw_points.main import raw_points_subcommands
from .resampled_points.main import resampled_points_subcommands


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
def main() -> None:
    pass


main.add_command(money_management_strategies_subcommands)
main.add_command(run_test)
main.add_command(raw_points_subcommands)
main.add_command(resampled_points_subcommands)


if __name__ == "__main__":
    main()
