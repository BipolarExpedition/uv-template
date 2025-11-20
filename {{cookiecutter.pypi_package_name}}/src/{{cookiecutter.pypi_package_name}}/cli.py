import typer
from rich import print

from . import PROJECT_COPYRIGHT, PROJECT_NAME, PROJECT_VERSION, __package__, __version__  # noqa: F401

app = typer.Typer(name=PROJECT_NAME, help=f"A command line interface for {PROJECT_NAME}")


def version_callback(value: bool):
    if value:
        print(f"{PROJECT_NAME} {__version__}")
        raise typer.Exit()


@app.command()
def main(
    version: bool | None = typer.Option(
        None, "--version", callback=version_callback, help="Print the version and exit", is_eager=True
    ),
):
    print(f"\n[cyan]This is the default action of [bold magenta]{PROJECT_NAME}[/bold magenta][/cyan]")

    print(f"\nReplace [green]this message[/green] by putting your code into {__package__}.cli:main")
    print("See Typer documentation at https://typer.tiangolo.com/")

    print(f"\nPossible default settings: {typer.get_app_dir(PROJECT_NAME)}")


if __name__ == "__main__":
    app()
