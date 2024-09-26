from util.Constants import Constants
from util.SqliteDatabase import SqliteDatabase


class DataManager:
    """Static class to manage database operations."""
    __db_instance = None

    @classmethod
    def initialize_database(cls, db_filename=Constants.DATABASE_NAME):
        if cls.__db_instance is None:
            cls.__db_instance = SqliteDatabase(db_filename)

    @classmethod
    def get_database(cls) -> SqliteDatabase:
        if cls.__db_instance is None:
            cls.initialize_database()
        return cls.__db_instance
