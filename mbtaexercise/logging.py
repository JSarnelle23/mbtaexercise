import logging
import sys
from logging.handlers import TimedRotatingFileHandler
from typing import Optional, Union

from . import __projectname__
from .utils import convert_to_seconds, validate_filepath
from .config import Config

def start_logger(config: Config) -> logging.Logger:
    logger = logging.getLogger(__projectname__)
    logger.setLevel(logging.getLevelName(str(config.LogLevel.value))) 
    
    if config.LogFile is not None:
        log_dir = validate_filepath(config.LogFile.LogDirectory)
        log_fp = log_dir / f"{__projectname__}.log"
        fh = TimedRotatingFileHandler(
            log_fp,
            interval=convert_to_seconds(config.LogFile.LogInterval), #type: ignore
            backupCount=config.LogFile.BackupCount
        )
        fh.setLevel(logging.getLevelName(config.LogFile.LogLevel.value))
        logger.addHandler(fh)
    
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.getLevelName(config.LogLevel.value))
    logger.addHandler(ch)
    
    return logger