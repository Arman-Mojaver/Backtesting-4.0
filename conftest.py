from _pytest.config import Config, Parser


def pytest_addoption(parser: Parser) -> None:
    parser.addoption(
        "--d",
        action="store_true",
        default=False,
        help="Run test in debug mode.",
    )


def pytest_collection_modifyitems(config: Config) -> None:
    if config.getoption("--d"):
        return
