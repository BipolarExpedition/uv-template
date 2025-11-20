from importlib import import_module
from pathlib import Path
from typer.testing import CliRunner

TestModuleBase = Path(__file__).parent.parent.stem.replace("-", "_")


def test_example_version():
    app = import_module(f"{TestModuleBase}.cli").app
    base = import_module(f"{TestModuleBase}")

    runner = CliRunner()

    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert base.PROJECT_VERSION in result.stdout.strip()
    assert base.PROJECT_NAME in result.stdout.strip()
    assert len(result.stdout.splitlines()) == 1
