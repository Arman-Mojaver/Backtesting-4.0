import sys
from pathlib import Path

import click

sys.path.append(Path(__file__).resolve().parent.parent.as_posix())


from .pytest.pytest_one import run_test


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
def main() -> None:
    pass


main.add_command(run_test)


if __name__ == "__main__":
    main()
