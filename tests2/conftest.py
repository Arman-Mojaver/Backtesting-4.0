import os

import pytest

os.environ["ENVIRONMENT"] = "testing"

from config import config as project_config  # type: ignore[attr-defined]

if not project_config.is_testing():
    err = f"Invalid testing environment: {project_config}"


@pytest.fixture
def go_server():
    """
    Equivalent to calling "localhost" from outside the container.
    Port is not needed since it is PORT=80.
    """
    return "http://host.docker.internal"


@pytest.fixture
def endpoint(go_server):
    def _endpoint(url):
        return f"{go_server}/{url}"

    return _endpoint
