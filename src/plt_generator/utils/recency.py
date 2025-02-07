from datetime import datetime
import json
import os
import time
from pathlib import Path


def get_time_created(path: Path | str) -> float:
    return os.path.getctime(path)


def time_created_readable(path: Path | str) -> str:
    time_created: time.struct_time = time.strptime(time.ctime(get_time_created(path)))
    return time.strftime("%Y-%m-%d %H:%M:%S", time_created)


def get_time_modified(path: Path | str) -> float:
    return os.path.getmtime(path)


def time_modified_readable(path: Path | str) -> str:
    time_modified: time.struct_time = time.strptime(time.ctime(get_time_modified(path)))
    return time.strftime("%Y-%m-%d %H:%M:%S", time_modified)


def first_newer(file1: str | Path, file2: str | Path | tuple[Path, ...] | tuple[str, ...]) -> bool:
    m1 = os.path.getmtime(file1)

    if isinstance(file2, tuple):
        m2 = max(os.path.getmtime(f) for f in file2)
    else:
        m2 = os.path.getmtime(file2)
    return m1 > m2


def make_timestamp() -> str:
    return f"{datetime.now():%Y-%m-%d_%H:%M:%S}"


def save_timestamp(key: str, timestamp_json: Path) -> None:
    with open(timestamp_json) as f:
        d = json.load(f)
    with open(timestamp_json, "w") as f:
        d.update({key: make_timestamp()})
        json.dump(d, f)
