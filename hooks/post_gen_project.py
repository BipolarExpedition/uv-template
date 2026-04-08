#!/usr/bin/env python

import os

if __name__ == "__main__":
    print("- Executing 'uv sync'")
    os.system("uv sync > /dev/null")
    print("- Generating initial git commit")
    os.system("git init > /dev/null")
    os.system('git add . > /dev/null && git commit -m "Initial commit from cookiecutter template" > /dev/null')
    print("\nYour Python package project has been created successfully!")
