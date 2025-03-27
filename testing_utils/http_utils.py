from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from requests import Response


def parse_response(response: Response) -> dict[Any, Any]:
    return json.loads(response.content.decode())
