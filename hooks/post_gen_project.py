#!/usr/bin/env python

import os

python_version = "{{ cookiecutter.python_version }}"

if __name__ == "__main__":
    print("- Executing 'uv sync --group dev'")
    os.system("uv sync --group dev > /dev/null")
    print("- Generating initial git commit")
    os.system("git init > /dev/null")
    os.system('git add . > /dev/null && git commit -m "Initial commit from cookiecutter template" > /dev/null')
    print("- Switching to 'dev' branch")
    os.system('git checkout -b dev')
    print(f"\nYour Python {python_version} project has been created successfully!")
