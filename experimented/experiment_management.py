import json
import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Callable, TypeVar, Generic

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


UserExperimentTVar = TypeVar("UserExperimentTVar")


class BaseExperimentMetadata(BaseModel):
    time_start: datetime
    time_end: datetime


class BaseExperiment(BaseModel, Generic[UserExperimentTVar]):
    metadata: BaseExperimentMetadata
    data: UserExperimentTVar


def get_experiment(path: Path) -> str:
    path = path / ".ex.json"
    with open(path) as file:
        return file.read()


def experiment_directories(store_path: Path) -> list[Path]:
    directories = [dir for dir in store_path.iterdir() if dir.is_dir()]
    return directories


def list_experiments_untyped(store_path: Path) -> list[tuple[Path, dict]]:
    experiments = [
        (dir, json.loads(get_experiment(dir)))
        for dir in experiment_directories(store_path)
    ]

    def _start_time(experiment: tuple[Path, dict]) -> datetime:
        try:
            ts = experiment[1].get("metadata", {}).get("time_start")
            return datetime.fromisoformat(ts) if ts is not None else datetime.min
        except Exception:
            return datetime.min

    return sorted(experiments, key=_start_time)


class Experiment(Generic[UserExperimentTVar]):
    def add_experiment(
        self,
        data: BaseExperiment[UserExperimentTVar],
        experiment_result: Path,
        store_path: Path | None = None,
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

    def list_experiments(
        self, store_path: Path
    ) -> list[tuple[Path, UserExperimentTVar]]:
        experiments_untyped = list_experiments_untyped(store_path)
        return [
            (
                experiment[0],
                BaseExperiment[UserExperimentTVar].model_validate(experiment[1]),
            )
            for experiment in experiments_untyped
        ]

    def filter_experiment(
        self,
        filter: Callable[[UserExperimentTVar], bool],
        store_path: Path | None = None,
    ) -> list[tuple[Path, UserExperimentTVar]]:
        if store_path is None:
            store_path = find_store()
        experiments = self.list_experiments(store_path)
        return [experiment for experiment in experiments if filter(experiment[1])]

    def delete_experiment(
        self, experiment_uuid: uuid.UUID, store_path: Path | None = None
    ) -> None:
        if store_path is None:
            store_path = find_store()
        shutil.rmtree(store_path / str(experiment_uuid))
