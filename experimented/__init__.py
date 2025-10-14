import os
import pprint
from pathlib import Path

import typer

from .experiment_management import find_store, list_experiments

app = typer.Typer()


@app.command()
def init(root_dir: Path | None = None) -> None:
    if root_dir is None:
        root_dir = Path(os.getcwd())
    experiment_store_path = root_dir / ".ex"
    print(f"Creating experiment store at {experiment_store_path}")
    os.makedirs(experiment_store_path)


@app.command()
def list(root_dir: Path | None = None) -> None:
    if root_dir is None:
        store_path = find_store()
    else:
        store_path = root_dir / ".ex"
    experiments = list_experiments(store_path)
    for idx, (dir, experiment) in enumerate(experiments):
        print(
            f"=== Experiment {idx}, "
            f"{experiment["metadata"]["time_start"]} "
            f"- {experiment["metadata"]["time_end"]} "
            f"{dir} ==="
        )
        pprint.pprint(experiment)
        print()


def main():
    app()
