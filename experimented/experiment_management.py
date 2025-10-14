import json
import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Callable

from pydantic import BaseModel
import uuid


def find_store() -> Path:
    """
    Find store location.
    traversing from cwd all the way back to root to find .ex folder
    """
    current = Path(os.getcwd())
    paths: list[Path] = [current] + list(current.parents)
    for path in paths:
        ex_path = path / ".ex"
        if ex_path.exists() and ex_path.is_dir():
            return ex_path
    raise RuntimeError("Cannot find experiment store.")


class BaseExperimentMetadata(BaseModel):
    time_start: datetime
    time_end: datetime


class BaseExperiment(BaseModel):
    metadata: BaseExperimentMetadata


def get_experiment(path: Path) -> str:
    path = path / ".ex.json"
    with open(path) as file:
        return file.read()


def experiment_directories(store_path: Path) -> list[Path]:
    directories = [dir for dir in store_path.iterdir() if dir.is_dir()]
    return directories


def list_experiments(store_path: Path) -> list[tuple[Path, dict]]:
    return [
        (dir, json.loads(get_experiment(dir)))
        for dir in experiment_directories(store_path)
    ]


def add_experiment(
    data: BaseExperiment, experiment_result: Path, store_path: Path | None = None
) -> uuid.UUID:
    if store_path is None:
        store_path = find_store()
    id_uuid = uuid.uuid4()
    print(str(id_uuid))
    path = store_path / str(id_uuid)
    shutil.copytree(experiment_result, path)
    with open(path / ".ex.json", "w") as file:
        json_txt = data.model_dump_json()
        file.write(json_txt)
    return id_uuid


def filter_experiment(
    filter: Callable[[dict], bool], store_path: Path | None = None
) -> list[tuple[Path, dict]]:
    if store_path is None:
        store_path = find_store()
    experiments = list_experiments(store_path)
    return [experiment for experiment in experiments if filter(experiment[1])]


def delete_experiment(
    experiment_uuid: uuid.UUID, store_path: Path | None = None
) -> None:
    if store_path is None:
        store_path = find_store()
    shutil.rmtree(store_path / str(experiment_uuid))


if __name__ == "__main__":
    add_experiment(
        data=BaseExperiment(
            metadata=BaseExperimentMetadata(
                time_start=datetime.now(), time_end=datetime.now()
            )
        ),
        store_path=find_store(),
        experiment_result=Path("test/hello"),
    )
    print(list_experiments(find_store()))
