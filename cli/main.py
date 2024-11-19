import click


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
def main() -> None:
    pass


if __name__ == "__main__":
    main()
