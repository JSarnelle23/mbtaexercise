import logging
import sqlite3 as sql
from .utils import validate_filepath

class SQLITE3Datastore:
    def __init__(self, log: logging.Logger, filepath: str):
        _fp = validate_filepath(filepath=filepath)
        self.db = sql.connect(_fp)
        self.init_db()

    def init_db(self):
        init_script="""

        """

    def close(self):
        self.db.commit()
        self.db.close()


    