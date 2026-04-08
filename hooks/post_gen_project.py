#!/usr/bin/env python

import os

if __name__ == "__main__":
    print("Executing 'uv sync'")
    os.system("uv sync")
    print("Generating initial git commit")
    os.system('git add . && git commit -m "Initial commit from cookiecutter template"')
    print("Your Python package project has been created successfully!")
