from pathlib import Path
from pydantic import BaseModel
import os
from datetime import datetime
from typing import Callable, Generic, TypeVar
import shutil
import json

def find_store() -> Path:
    """Find store location, traversing from cwd all the way back to root to find .ex folder"""
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

def list_experiments(store_path: Path) -> list[dict]:
    return [json.loads(get_experiment(dir)) for dir in experiment_directories(store_path)]

def add_experiment(data: BaseExperiment, experiment_result: Path, store_path: Path | None) -> None:
    if store_path is None:
        store_path = find_store()
    id = len(experiment_directories(store_path))
    path = store_path / str(id)
    shutil.copytree(experiment_result, path)
    with open(path / ".ex.json", "w") as file:
        json_txt = data.model_dump_json()
        file.write(json_txt)

def filter_experiment(filter:Callable[[dict], bool], store_path: Path | None) -> list[dict]:
    if store_path is None:
        store_path = find_store()
    experiments = list_experiments(store_path)
    return [experiment for experiment in experiments if filter(experiment)]

if __name__ == "__main__":
    add_experiment(data=BaseExperiment(metadata=BaseExperimentMetadata(time_start=datetime.now(), time_end=datetime.now())), store_path=find_store(), experiment_result=Path("hello"))
    print(list_experiments(find_store()))
