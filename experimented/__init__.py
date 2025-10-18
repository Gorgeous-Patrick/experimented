import os
import pprint
from pathlib import Path

import typer

from .experiment_management import (
    list_experiments_untyped,
    find_store,
    BaseExperiment,
    Experiment,
)

app = typer.Typer()


@app.command()
def init(experiment_root_dir: Path | None = None) -> None:
    if experiment_root_dir is None:
        experiment_root_dir = Path(os.getcwd())
    experiment_store_path = experiment_root_dir / ".ex"
    print(f"Creating experiment store at {experiment_store_path}")
    os.makedirs(experiment_store_path)


@app.command()
def ls(experiment_root_dir: Path | None = None) -> None:
    if experiment_root_dir is None:
        store_path = find_store()
    else:
        store_path = experiment_root_dir / ".ex"
    experiments = list_experiments_untyped(store_path)
    for idx, (dir, experiment) in enumerate(experiments):
        print(
            f"=== Experiment {idx}, "
            f"{experiment["metadata"]["time_start"]} "
            f"- {experiment["metadata"]["time_end"]} "
            f"{dir} ==="
        )
        pprint.pprint(experiment)
        print()


__all__ = ["BaseExperiment", "Experiment"]


def main():
    app()
