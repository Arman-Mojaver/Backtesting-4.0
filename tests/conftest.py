import os

from _pytest.config import Config, Parser

os.environ["ENVIRONMENT"] = "testing"


from config import config as project_config

if not project_config.is_testing():
    err = f"Invalid testing environment: {project_config}"
    raise ValueError(err)


def pytest_addoption(parser: Parser) -> None:
    parser.addoption(
        "--integration",
        action="store_true",
        default=False,
        help="Run integration tests.",
    )
    parser.addoption(
        "--d",
        action="store_true",
        default=False,
        help="Run test in debug mode.",
    )


def pytest_collection_modifyitems(config: Config) -> None:
    if config.getoption("--integration"):
        return

    if config.getoption("--d"):
        return
