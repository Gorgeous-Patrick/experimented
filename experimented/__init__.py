import os
import pprint
from pathlib import Path
from uuid import UUID

import typer

from .experiment_management import (
    add_experiment,
    delete_experiment,
    filter_experiment,
    find_store,
    list_experiments,
    BaseExperiment,
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


@app.command()
def add(
    experiment_dir: Path, experiment_info: Path, experiment_root_dir: Path | None = None
) -> None:
    if experiment_root_dir is None:
        experiment_root_dir = Path(os.getcwd())
    store_path = experiment_root_dir / ".ex"
    with open(experiment_info) as file:
        # Make sure that the experiment info can be interpreted as BaseExperiment
        data = BaseExperiment.model_validate_json(file.read())
    add_experiment(data, experiment_dir, store_path)


@app.command()
def rm(experiment_idx: UUID, experiment_root_dir: Path | None = None) -> None:
    if experiment_root_dir is None:
        experiment_root_dir = Path(os.getcwd())
    store_path = experiment_root_dir / ".ex"
    delete_experiment(experiment_idx, store_path)
    print(f"Experiment {experiment_idx} removed.")


__all__ = ["list_experiments", "filter_experiment", "add_experiment"]


def main():
    app()
