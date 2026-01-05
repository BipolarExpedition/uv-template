import os
import shutil
import tempfile
from pathlib import Path
from subprocess import run  #, CalledProcessError

script_dir = Path(__file__).parent.resolve()

temp_dir = tempfile.mkdtemp(prefix="uv-template-test-")
try:
    print(f"Temporary directory created at: {temp_dir}")
    print()

    os.chdir(temp_dir)
    print(f"Changed working directory to: {Path.cwd()}")

    print(f"Invoking cookiecutter with: --no-input {script_dir.parent.resolve()}")
    run(
        ["cookiecutter",
            "--no-input",
            str(script_dir.parent.resolve()),
        ],
        check=True
    )

    # project should be in the only generated subdirectory
    generated_dirs = [d for d in Path(temp_dir).iterdir() if d.is_dir()]
    os.chdir(generated_dirs[0])
    print(f"Changed working directory to generated project: {Path.cwd()}")

    print("Running tests with 'uv run pytest -v'")
    run(
        ["uv", "run", "pytest", "-v"],
        check=True
    )



finally:
    shutil.rmtree(temp_dir)
    print(f"Temporary directory {temp_dir} removed.")