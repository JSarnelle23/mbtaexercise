from enum import Enum
from typing import Optional

from pydantic import BaseModel

from .utils import validate_filepath

#from typing import Optional


class LogLevel(str, Enum):
    critical = CRITICAL = "CRITICAL"
    error = ERROR = "ERROR"
    warning = WARNING = "WARNING"
    warn = WARN = "WARN"
    info = INFO = "INFO"
    debug = DEBUG = "DEBUG"

class LogFileConfig(BaseModel):
    LogDirectory: str
    LogLevel: LogLevel
    LogInterval: str
    BackupCount: int 


class Config(BaseModel):
    Period: str
    Count: int
    MaxBurst: int
    DatabasePath: str
    LogLevel: LogLevel
    LogFile: Optional[LogFileConfig]
   

def get_config(filepath: str):
    fp = validate_filepath(filepath)
    config = Config.parse_file(fp)
    return config
