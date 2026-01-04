from logging import log
import re
from pathlib import Path

import typer
from rich import print  # noqa: A004

from . import PROJECT_COPYRIGHT, PROJECT_NAME, PROJECT_VERSION, __version__  # noqa: F401

from .logging import configure_logging

# from pydantic import BaseModel, SecretStr
# class Config(BaseModel):
#     api_key: SecretStr
#     db_password: SecretStr

app = typer.Typer(name=PROJECT_NAME, help=f"A command line interface for {PROJECT_NAME}")


def version_callback(value: bool) -> None:
    if value:
        print(f"{PROJECT_NAME} {__version__}")
        raise typer.Exit()

def do_configure_logging(is_verbose: bool,
        is_debug: bool, 
        do_log_file: bool = True
    ) -> None:

    console_level = "WARNING"
    log_level = "WARNING"
    console_tracebacks = False
    console_show_locals = False
    console_show_time = False

    if is_verbose:
        console_level = "INFO"
        log_level = "INFO"
    if is_debug:
        console_level = "DEBUG"
        log_level = "DEBUG"
        console_tracebacks = True
        console_show_locals = True
        console_show_time = True

    logfile_name: Path = Path(".") / re.sub(r"[^a-zA-Z0-9]", "_", "{PROJECT_NAME.lower()") + ".log"

    configure_logging(level=log_level, console_level=console_level,
            log_file=logfile_name.resolve(),
            console_tracebacks=console_tracebacks,
            console_show_time=console_show_time,
            loguru_tracebacks=console_tracebacks,
            loguru_locals=console_show_locals,
            console_locals=console_show_locals,
            console_show_time=console_show_time
        )

@app.command()
def main(
    version: bool | None = typer.Option(
        None, "--version", callback=version_callback, help="Print the version and exit", is_eager=True
    ),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose output"),
    debug: bool = typer.Option(False, "--debug", "-d", help="Enable debug output")
) -> None:

    do_configure_logging(verbose, debug)

    print(f"\n[cyan]This is the default action of [bold magenta]{PROJECT_NAME}[/bold magenta][/cyan]")

    print(f"\nReplace [green]this message[/green] by putting your code into {__package__}.cli:main")
    print("See Typer documentation at https://typer.tiangolo.com/")

    print(f"\nPossible default settings: {typer.get_app_dir(PROJECT_NAME)}")


if __name__ == "__main__":
    app()
