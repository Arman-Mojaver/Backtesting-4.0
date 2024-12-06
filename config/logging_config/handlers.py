from __future__ import annotations

import logging
from typing import ClassVar


class ColorizingStreamHandler(logging.StreamHandler):
    """
    A stream handler which supports colorizing of console streams
    under Windows, Linux and Mac OS X.
    """

    # color names to indices
    color_map: ClassVar = {
        "default": 9,
        "black": 0,
        "red": 1,
        "green": 2,
        "yellow": 3,
        "blue": 4,
        "magenta": 5,
        "cyan": 6,
        "white": 7,
    }

    # levels to (background, foreground, bold/intense)
    level_map: ClassVar = {
        logging.DEBUG: (None, "green", False),
        logging.INFO: (None, "default", False),
        logging.WARNING: (None, "yellow", False),
        logging.ERROR: (None, "red", False),
        logging.CRITICAL: ("red", "white", True),
    }

    csi = "\x1b["
    reset = "\x1b[0m"

    @property
    def is_tty(self) -> bool:
        """Return true if the handler's stream is a terminal."""
        isatty = getattr(self.stream, "isatty", False)
        return isatty and isatty()  # type: ignore[misc]

    def emit(self, record: logging.LogRecord) -> None:
        try:
            message = self.format(record)
            stream = self.stream

            stream.write(message)
            stream.write(getattr(self, "terminator", "\n"))
            self.flush()
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception:  # noqa: BLE001
            self.handle_logging_error(record)

    def handle_logging_error(self, record: logging.LogRecord) -> None:
        self.handleError(record)

    def colorize(self, message: str, record: logging.LogRecord) -> str:
        """
        Colorize a message for a logging event.

        This implementation uses the ``level_map`` class attribute to
        map the LogRecord's level to a colour/intensity setting, which is
        then applied to the whole message.
        """
        if record.levelno in self.level_map:
            bg, fg, bold = self.level_map[record.levelno]
            params = []
            if bg in self.color_map:
                params.append(str(self.color_map[bg] + 40))
            if fg in self.color_map:
                params.append(str(self.color_map[fg] + 30))
            if bold:
                params.append("1")
            if params:
                message = "".join((self.csi, ";".join(params), "m", message, self.reset))
        return message

    def format(self, record: logging.LogRecord) -> str:
        """
        Format a record for output.

        This implementation colorizes the message line, but leaves
        any traceback uncolored.
        """
        message = logging.StreamHandler.format(self, record)
        if self.is_tty:
            # Don't colorize any traceback
            parts = message.split("\n", 1)
            parts[0] = self.colorize(parts[0], record)
            message = "\n".join(parts)
        return message
