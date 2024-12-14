from typing import Iterator


class InvalidRangeInputsError(Exception):
    """Error raised when start, stop and step values are invalid."""


MIN_START_STOP = 0.1


def _validate_range_inputs(start: float, stop: float, step: float) -> None:
    if start <= MIN_START_STOP or stop <= MIN_START_STOP or step <= 0:
        err = "range values must be a positive integer"
        raise InvalidRangeInputsError(err)


def frange(start: float, stop: float, step: float) -> Iterator[float]:
    _validate_range_inputs(start=start, stop=stop, step=step)

    while start < stop:
        yield round(start, 10)  # Round to avoid floating-point precision issues
        start += step
