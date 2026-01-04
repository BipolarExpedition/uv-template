from io import StringIO
from pathlib import Path
from typing import Any

import pytest
from cookiecutter.main import cookiecutter

TEMPLATE_PATH = r"."

test_params = [
    # {
    #     "input_context": {
    #     },
    #     "input_lines": [],
    #     "expected_files" : [],
    #     "expected_contents": [],
    #     "expected_exceptions": [],
    # },
    pytest.param(
        {
            "input_context": {
                "project_name": "A project with spaces",
            },
            "input_lines": [
                "",
                "",
                "",  # 1-3
                "A project with spaces",  # 4
                "",
                "",
                "",
                ""  # 5-8
                "",
                "",
                "",  # 9-11
                "",
            ],
            "expected_files": [
                "README.md",
                "src/a_project_with_spaces/__init__.py",
            ],
            "expected_contents": [
                ("README.md", "# A project with spaces"),
                ("pyproject.toml", 'name = "a-project-with-spaces"'),
            ],
            "expected_exceptions": [],
        },
        id="project_name_with_spaces",
    ),
    pytest.param(
        {
            "input_context": {"project_name": "project_with_üñíçødé"},
            "expected_files": [],
            "input_lines": [
                "",
                "",
                "",
                "project_with_üñíçødé",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
            ],
            "expected_contents": [],
            "expected_exceptions": [Exception],
        },
        id="invalid_module_name",
    ),
]


@pytest.mark.parametrize("test_case", test_params)
def test_template_generation(test_case: dict[str, Any], tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    print(f"Using temporary path for test: {tmp_path}")
    context = test_case["input_context"]

    # clean_lines: str = "\n".join([line.strip() for line in test_case.get("input_lines", [])])
    # tlist = [line.strip() for line in test_case.get("input_lines", [])]
    # clean_lines = iter(tlist)

    no_input = True

    if "input_lines" in test_case:
        tstring = "\n".join(test_case.get("input_lines", [])) + "\n"
        stream_input = StringIO(tstring)
        monkeypatch.setattr("sys.stdin", stream_input)
        no_input = False

    # Generate the project using cookiecutter
    if "expected_exceptions" in test_case and test_case["expected_exceptions"]:
        with pytest.raises(tuple(test_case["expected_exceptions"])):
            cookiecutter(
                str(TEMPLATE_PATH), no_input=no_input, extra_context=context, output_dir=str(tmp_path.resolve())
            )
        return
    else:
        project_path = cookiecutter(
            str(TEMPLATE_PATH), no_input=no_input, extra_context=context, output_dir=str(tmp_path.resolve())
        )

    generated_project = Path(project_path).resolve()

    # Check that the project directory was created
    assert generated_project.exists()
    assert generated_project.is_dir()

    # Check for expected files and directories
    for file in test_case["expected_files"]:
        file_path = generated_project / file
        assert file_path.exists(), f"Expected file {file} does not exist."

    for file, expected_content in test_case["expected_contents"]:
        file_path = generated_project / file
        assert file_path.exists(), f"Expected file {file} does not exist."
        with file_path.open() as f:
            content = f.read()
            assert expected_content in content, f"Content '{expected_content}' not found in {file}."
