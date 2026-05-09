import re
from pathlib import Path

import typer
from rich import print  # noqa: A004

from . import PROJECT_COPYRIGHT, PROJECT_NAME, PROJECT_VERSION, __version__  # noqa: F401
from .configuration import Settings
from .mylogging import logger, setup_logging
from .experiments import EXPERIMENT_LIST

# from pydantic import BaseModel, SecretStr
# class Config(BaseModel):
#     api_key: SecretStr
#     db_password: SecretStr

app = typer.Typer(name=PROJECT_NAME, help=f"A command line interface for {PROJECT_NAME}")


def version_callback(value: bool) -> None:
    if value:
        print(f"{PROJECT_NAME} {__version__}")
        raise typer.Exit()


@app.callback(invoke_without_command=True)
def common(
    ctx: typer.Context,
    version: bool = typer.Option(None, "--version", callback=version_callback, is_eager=True),
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Enable verbose output", envvar=f"{PROJECT_NAME.upper()}_VERBOSE".upper()
    ),
    debug: bool = typer.Option(False, "--debug", "-d", help="Enable debug output", envvar=f"{PROJECT_NAME.upper()}_DEBUG".upper()),
):
    """Function always called when the CLI tool is launched"""

    do_configure_logging(verbose, debug)
    logger.debug("Debug logging is enabled")
    logger.info(f"Starting {PROJECT_NAME} version {PROJECT_VERSION}")

    logger.debug("Loading configuration")
    config = Settings.load()  # noqa: F841
    # config = Settings.load(Path() / "ollamaphiles.toml")  # noqa: F841

    # If no command was used, run the default "main"
    if ctx.invoked_subcommand is None:
        main(ctx)


def do_configure_logging(is_verbose: bool, is_debug: bool, do_log_file: bool = True) -> None:
    """Setup default logging"""

    console_level = "WARNING"
    log_level = "WARNING"
    console_tracebacks = False
    console_show_locals = False
    console_show_path = False
    console_show_time = False

    if is_verbose:
        console_level = "INFO"
        log_level = "INFO"
    if is_debug:
        console_level = "DEBUG"
        log_level = "DEBUG"
        console_tracebacks = True
        console_show_locals = True
        console_show_path = True
        console_show_time = True

    logfile_name: Path = Path().joinpath(re.sub(r"[^a-zA-Z0-9]", "_", PROJECT_NAME.lower()) + ".log")

    setup_logging(
        level=log_level,
        console_level=console_level,
        log_file=str(logfile_name.resolve()),
        console_tracebacks=console_tracebacks,
        console_show_time=console_show_time,
        console_locals=console_show_locals,
        console_show_path=console_show_path,
        loguru_tracebacks=console_tracebacks,
        loguru_locals=console_show_locals,
    )

@app.command()
def main(
    ctx: typer.Context = None,  # type: ignore
) -> None:
    """Program entry point if there not commands are chosen"""

    print(f"\n[cyan]This is the default action of [bold magenta]{PROJECT_NAME}[/bold magenta][/cyan]")
    print("")
    print(f"Replace [green]this message[/green] by putting your code into {__package__}.cli:main")
    print("See Typer documentation at [bold yellow]https://typer.tiangolo.com/[/bold yellow]\n\n")

    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")

    if ctx is None:
        # If we call main directly, enable all logging
        do_configure_logging(True, True)
        logger.warning("main() called directly")

    return

@app.command(name="experiment")
def experiment(experiment_name: str = typer.Argument(help="Name of the experiment to run")) -> None:
    """CLI handler for 'experiment' command.

    Launching the program with the command 'experiment', followed by the name of the experiment,
    will launch those experiments defined in .experiments.EXPERIMENT_LIST
    """

    chosen_experiment = experiment_name.strip().lower()
    if chosen_experiment in EXPERIMENT_LIST:
        EXPERIMENT_LIST[chosen_experiment]()
    else:
        logger.error(f"The experiment '{chosen_experiment}' does not exist.")
    return


if __name__ == "__main__":
    app()
