from typing import Union, Optional
from pathlib import Path
import os
from itertools import chain, islice


def convert_to_seconds(s: Union[str,int], unit_table={"s":1, "m": 60, "h":3600, "d": 86400, "w":604800}) -> int:
    if isinstance(s, int):
        return s
    if isinstance(s, str) and s.isnumeric():
        return int(s)
    if isinstance(s, str):
        s = s.lower()
    return int(s[:-1]) * unit_table[s[-1]]


def chunk(iterlike, chunk_size):
    iterlike = iter(iterlike)
    for i in iterlike:
        yield filter(None, chain((i,), islice(iterlike, chunk_size - 1)))


def validate_filepath(filepath: str) -> Path:
    fp = Path(filepath)
    if fp.is_dir() and not fp.exists():
        os.makedirs(fp, mode=0o750, exist_ok=True)
        return fp
    if fp.is_file():
        if not fp.parent.exists():
            os.makedirs(fp.parent, mode=0o750, exist_ok=True)
    return fp