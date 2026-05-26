from pathlib import Path


def create_directories():

    directories = [
        "data/raw",
        "data/interim",
        "data/processed",
        "artifacts/preprocessing",
        "logs",
        "tests"
    ]

    for directory in directories:
        Path(directory).mkdir(
            parents=True,
            exist_ok=True
        )