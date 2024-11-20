from __future__ import annotations

import subprocess


def collect_pytests() -> list[str]:
    command = ["pytest", "--collect-only", "-q"]

    tests_bytes = subprocess.check_output(command, stderr=subprocess.STDOUT, text=True)  # noqa: S603
    return tests_bytes.strip().split("\n")[
        :-2
    ]  # There are two extra lines in the end that we do not need


def run_pytest_test_by_name(
    name: str,
    *,
    debug: bool = False,
    print_: bool = False,
    verbose: bool = False,
) -> None:
    command = ["pytest", "-k", name]

    if debug:
        command.append("--d")

    if print_:
        command.append("-s")

    if verbose:
        command.append("-vv")

    subprocess.run(command, check=True)  # noqa: S603


def run_pytest_test_by_file_name(
    file_name: str,
    *,
    print_: bool = False,
    verbose: bool = False,
) -> None:
    command = ["pytest", file_name]

    if print_:
        command.append("-s")

    if verbose:
        command.append("-vv")

    subprocess.run(command, check=True)  # noqa: S603
