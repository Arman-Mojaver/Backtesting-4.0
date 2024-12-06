import click


def confirm(
    message: str,
    color: str = "red",
    *,
    abort: bool = True,
    yes: bool = False,
) -> bool:
    if yes:
        click.echo(click.style(message, fg=color) + " y")
        return True

    return click.confirm(click.style(message, fg=color), abort=abort)
