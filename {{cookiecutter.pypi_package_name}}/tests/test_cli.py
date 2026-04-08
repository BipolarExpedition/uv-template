from pathlib import Path

from typer.testing import CliRunner

import {{ cookiecutter.project_slug }} as base
from {{ cookiecutter.project_slug }}.cli import app

TestModuleBase = Path(__file__).parent.parent.stem.replace("-", "_")


def test_example_version():
    runner = CliRunner()

    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert base.PROJECT_VERSION in result.stdout.strip()
    assert base.PROJECT_NAME in result.stdout.strip()
    assert len(result.stdout.splitlines()) == 1
