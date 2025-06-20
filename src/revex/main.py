import click
import revex.parser
import json

VERSION = "1.0.0"


@click.command()
@click.argument("input", type=str, required=False, default=None)
@click.option("--version", is_flag=True, help="Show the version of Revex.")
@click.option(
    "--config",
    type=str,
    default='{"max_repeats": 3}',
    help="Configuration for the generator in JSON format.",
)
@click.option(
    "--debug",
    is_flag=True,
    help="Enable debug mode for more verbose output.",
)
def main(input, version, config, debug):
    """Revex CLI tool."""

    if version:
        click.echo(f"Revex version {VERSION}")
        return

    if input is not None:
        parser = revex.parser.Parser()
        # try:
        generator = parser.parse(input)
        result = generator.generate(json.loads(config))
        if debug:
            click.echo(f"Debug AST:\n {generator}")
        click.echo(f"{result}")
        # except Exception as e:
        #     click.echo(f"Error parsing input: {e}")


if __name__ == "__main__":
    main()
