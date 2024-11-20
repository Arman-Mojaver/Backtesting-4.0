from __future__ import annotations

from pprint import pprint

import click

from testing_utils import (
    collect_pytests,
    run_pytest_test_by_file_name,
    run_pytest_test_by_name,
)


@click.command("test", help="Run test, provided its name")
@click.argument("test_name", required=False)
@click.option(
    "-d",
    "--debug",
    type=bool,
    default=False,
    is_flag=True,
    help="Run test in debug mode",
)
@click.option(
    "-s",
    "--print",
    "print_",
    type=bool,
    default=False,
    is_flag=True,
    help="Print all the tests",
)
@click.option(
    "-f",
    "--file",
    "file_name",
    type=str,
    default="",
    help="Run test file",
)
@click.option(
    "-vv",
    "--verbose",
    type=bool,
    default=False,
    is_flag=True,
    help="Display more verbosely",
)
def run_test(
    test_name: str | None,
    file_name: str,
    *,
    debug: bool,
    print_: bool,
    verbose: bool,
) -> None:
    test_paths = collect_pytests()
    test_names = [test.split("::")[-1] for test in test_paths]

    if file_name:
        run_pytest_test_by_file_name(file_name=file_name, print_=print_, verbose=verbose)
        return

    if not test_name:
        pprint(test_names)  # noqa: T203
        return

    matches = [test for test in test_names if test_name in test]

    if len(matches) == 1:
        run_pytest_test_by_name(
            name=matches[0],
            debug=debug,
            print_=print_,
            verbose=verbose,
        )

    if len(matches) > 1:
        print(f"Several matches: {len(matches)}. Rename the test")  # noqa: T201
        pprint(matches)  # noqa: T203

    if len(matches) == 0:
        print(f"No matches: {test_name}")  # noqa: T201


if __name__ == "__main__":
    run_test()
