from __future__ import annotations

import subprocess
import time

import requests
from requests.auth import HTTPBasicAuth


def get_states() -> list[str]:
    all_states = []
    for _ in range(20):
        response = requests.get(
            "http://localhost:5555/api/tasks",
            auth=HTTPBasicAuth("admin", "admin"),
            timeout=5,
        )
        states = [value["state"] for value in response.json().values()]
        all_states.extend(states)
        time.sleep(0.5)

    return all_states


def run_timer() -> None:
    print("Starting timer")  # noqa: T201
    while True:
        all_states = get_states()
        task_is_ongoing = any(state == "STARTED" for state in all_states)
        if not task_is_ongoing:
            break

        time.sleep(600)

    print("Putting laptop to sleep")  # noqa: T201
    time.sleep(3)
    subprocess.run(["shutdown", "-s", "now"], check=False)  # noqa: S603, S607


if __name__ == "__main__":
    run_timer()
