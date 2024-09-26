import logging

from PyQt6.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel

from util.Constants import Constants, DATABASE_MESSAGE


class SqliteDatabase:
    def __init__(self, db_filename=Constants.DATABASE_NAME):
        self.initialize_vars(db_filename)
        self.initialize_db()
        logging.basicConfig(level=logging.INFO)

    def initialize_vars(self, db_filename):
        self.db_filename = db_filename
        self.db = None
        self.model = None

        # Vision
        self.vision_main_table_name = Constants.VISION_MAIN_TABLE
        self.vision_detail_table_name = Constants.VISION_DETAIL_TABLE

        # Vision File
        self.vision_file_table_name = Constants.VISION_FILE_TABLE

    def initialize_db(self):
        self.db = QSqlDatabase.addDatabase(Constants.SQLITE_DATABASE)
        self.db.setDatabaseName(self.db_filename)
        if not self.db.open():
            print(f"{DATABASE_MESSAGE.DATABASE_FAILED_OPEN}")
            return

        self.enable_foreign_key()
        self.create_all_tables()

    def enable_foreign_key(self):
        query = QSqlQuery(db=self.db)
        query_string = DATABASE_MESSAGE.DATABASE_PRAGMA_FOREIGN_KEYS_ON
        if not query.exec(query_string):
            print(f"{DATABASE_MESSAGE.DATABASE_ENABLE_FOREIGN_KEY} {query.lastError().text()}")

    def setup_model(self, table_name, filter=""):
        self.model = QSqlTableModel(db=self.db)
        self.model.setTable(table_name)
        self.model.setEditStrategy(QSqlTableModel.EditStrategy.OnManualSubmit)
        if filter:
            self.model.setFilter(filter)
        self.model.select()

    def create_all_tables(self):
        self.create_vision_main()
        self.create_vision_file()

    def create_vision_main(self):
        query = QSqlQuery()
        query_string = f"""
                        CREATE TABLE IF NOT EXISTS {self.vision_main_table_name} 
                         (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            title TEXT NOT NULL,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
                        )
                        """
        try:
            query.exec(query_string)
        except Exception as e:
            print(f"{DATABASE_MESSAGE.DATABASE_VISION_CREATE_TABLE_ERROR} {e}")

    def add_vision_main(self, title):
        query = QSqlQuery()
        query.prepare(f"INSERT INTO {self.vision_main_table_name} (title) VALUES (:title)")
        query.bindValue(":title", title)
        try:
            if query.exec():
                vision_main_id = query.lastInsertId()
                self.create_vision_detail(vision_main_id)
                return vision_main_id
        except Exception as e:
            print(f"{DATABASE_MESSAGE.DATABASE_VISION_ADD_ERROR} {e}")
        return None

    def update_vision_main(self, id, title):
        query = QSqlQuery()
        query.prepare(f"UPDATE {self.vision_main_table_name} SET title = :title WHERE id = :id")
        query.bindValue(":title", title)
        query.bindValue(":id", id)
        try:
            if query.exec():
                return True
        except Exception as e:
            print(f"{DATABASE_MESSAGE.DATABASE_VISION_UPDATE_ERROR} {e}")
        return False

    def delete_vision_main_entry(self, id):
        try:
            query = QSqlQuery()
            query.prepare(f"DELETE FROM {self.vision_main_table_name} WHERE id = :id")
            query.bindValue(":id", id)
            if not query.exec():
                raise Exception(query.lastError().text())
            logging.info(f"{DATABASE_MESSAGE.DATABASE_VISION_MAIN_ENTRY_SUCCESS} {id}")
        except Exception as e:
            logging.error(f"{DATABASE_MESSAGE.DATABASE_VISION_MAIN_ENTRY_FAIL} {id}: {e}")
            return False
        return True

    def delete_vision_detail(self, id):
        try:
            query = QSqlQuery()
            table_name = f"{self.vision_detail_table_name}_{id}"
            query.prepare(f"DROP TABLE IF EXISTS {table_name}")
            if not query.exec():
                raise Exception(query.lastError().text())
            logging.info(f"{DATABASE_MESSAGE.DATABASE_DELETE_DETAIL_TABLE_SUCCESS} {table_name}")
        except Exception as e:
            logging.error(f"{DATABASE_MESSAGE.DATABASE_DELETE_DETAIL_TABLE_ERROR} {id}: {e}")
            return False
        return True

    def delete_vision_main(self, id):
        try:
            if not self.delete_vision_detail(id):
                raise Exception(f"Failed to delete vision details for id {id}")
            if not self.delete_vision_main_entry(id):
                raise Exception(f"Failed to delete vision main entry for id {id}")
        except Exception as e:
            logging.error(f"Error deleting vision main for id {id}: {e}")
            return False
        return True

    def get_all_vision_main_list(self):
        query = QSqlQuery()
        query.prepare(f"SELECT * FROM {self.vision_main_table_name} ORDER BY created_at DESC")
        try:
            if query.exec():
                results = []
                while query.next():
                    id = query.value(0)
                    title = query.value(1)
                    created_at = query.value(2)
                    results.append({'id': id, 'title': title, 'created_at': created_at})
                return results
        except Exception as e:
            print(f"{DATABASE_MESSAGE.DATABASE_RETRIEVE_DATA_FAIL} {self.vision_main_table_name}: {e}")
        return []

    def create_vision_detail(self, vision_main_id):
        query = QSqlQuery()
        vision_detail_table = f"{self.vision_detail_table_name}_{vision_main_id}"
        query_string = f"""
                        CREATE TABLE IF NOT EXISTS {vision_detail_table} 
                         (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            vision_main_id TEXT, 
                            vision_type TEXT,
                            vision_model TEXT,
                            vision_text TEXT,
                            elapsed_time TEXT, 
                            finish_reason TEXT,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
                            FOREIGN KEY(vision_main_id) REFERENCES {self.vision_main_table_name}(id) ON DELETE CASCADE
                        )
                        """
        try:
            query.exec(query_string)
        except Exception as e:
            print(f"{DATABASE_MESSAGE.DATABASE_VISION_DETAIL_CREATE_TABLE_ERROR} {e}")

    def get_all_vision_details_list(self, vision_main_id):
        vision_detail_table = f"{self.vision_detail_table_name}_{vision_main_id}"
        query = QSqlQuery()
        query.prepare(f"SELECT * FROM {vision_detail_table}")

        try:
            if not query.exec():
                print(
                    f"{DATABASE_MESSAGE.DATABASE_VISION_DETAIL_FETCH_ERROR} {vision_main_id}: {query.lastError().text()}")
                return []
        except Exception as e:
            print(f"{DATABASE_MESSAGE.DATABASE_EXECUTE_QUERY_ERROR} {e}")
            return []

        vision_details_list = []
        while query.next():
            vision_detail = {
                "id": query.value("id"),
                "vision_main_id": query.value("vision_main_id"),
                "vision_type": query.value("vision_type"),
                "vision_model": query.value("vision_model"),
                "vision_text": query.value("vision_text"),
                "elapsed_time": query.value("elapsed_time"),
                "finish_reason": query.value("finish_reason"),
                "created_at": query.value("created_at")
            }
            vision_details_list.append(vision_detail)

        return vision_details_list

    def insert_vision_detail(self, vision_main_id, vision_type, vision_model, vision_text,
                             elapsed_time, finish_reason):
        vision_detail_table = f"{self.vision_detail_table_name}_{vision_main_id}"
        query = QSqlQuery()
        query.prepare(
            f"INSERT INTO {vision_detail_table} (vision_main_id, vision_type, vision_model, vision_text, "
            f" elapsed_time, finish_reason) "
            f" VALUES (:vision_main_id, :vision_type, :vision_model, :vision_text, "
            f" :elapsed_time, :finish_reason)")
        query.bindValue(":vision_main_id", vision_main_id)
        query.bindValue(":vision_type", vision_type)
        query.bindValue(":vision_model", vision_model)
        query.bindValue(":vision_text", vision_text)
        query.bindValue(":elapsed_time", elapsed_time)
        query.bindValue(":finish_reason", finish_reason)
        try:
            if query.exec():
                vision_detail_id = query.lastInsertId()
                return f"{vision_detail_table}_{vision_detail_id}"
            else:
                error = query.lastError()
                print(f"{DATABASE_MESSAGE.DATABASE_VISION_DETAIL_INSERT_ERROR} {error.text()}")
                return False
        except Exception as e:
            print(f"{DATABASE_MESSAGE.DATABASE_VISION_DETAIL_INSERT_ERROR} {e}")
            return False

    def create_vision_file(self):
        query = QSqlQuery()
        vision_detail_file_table = f"{self.vision_file_table_name}"
        query_string = f"""
                        CREATE TABLE IF NOT EXISTS {vision_detail_file_table} 
                         (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            vision_detail_id TEXT, 
                            vision_detail_file_data BLOB,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
                        )
                        """
        try:
            query.exec(query_string)
        except Exception as e:
            print(f"{DATABASE_MESSAGE.DATABASE_VISION_DETAIL_FILE_CREATE_TABLE_ERROR} {e}")

    def get_all_vision_details_file_list(self, vision_detail_id):
        vision_detail_file_table = f"{self.vision_file_table_name}"
        query = QSqlQuery()
        query.prepare(f"SELECT * FROM {vision_detail_file_table} WHERE vision_detail_id = :vision_detail_id")
        query.bindValue(":vision_detail_id", vision_detail_id)

        try:
            if not query.exec():
                print(f"{DATABASE_MESSAGE.DATABASE_VISION_DETAIL_FILE_FETCH_ERROR} {vision_detail_id}: "
                      f" {query.lastError().text()}")
                return []
        except Exception as e:
            print(f"{DATABASE_MESSAGE.DATABASE_EXECUTE_QUERY_ERROR} {e}")
            return []

        vision_detail_file_list = []
        while query.next():
            vision_detail = {
                "id": query.value("id"),
                "vision_detail_id": query.value("vision_detail_id"),
                "vision_detail_file_data": query.value("vision_detail_file_data"),
                "created_at": query.value("created_at")
            }
            vision_detail_file_list.append(vision_detail)

        return vision_detail_file_list

    def insert_vision_file(self, vision_detail_id, vision_detail_file_data):
        vision_detail_file_table = f"{self.vision_file_table_name}"
        query = QSqlQuery()
        query.prepare(
            f"INSERT INTO {vision_detail_file_table} (vision_detail_id, vision_detail_file_data) "
            f" VALUES (:vision_detail_id, :vision_detail_file_data)")
        query.bindValue(":vision_detail_id", vision_detail_id)
        query.bindValue(":vision_detail_file_data", vision_detail_file_data)
        try:
            success = query.exec()
            if not success:
                print(f"{DATABASE_MESSAGE.DATABASE_EXECUTE_QUERY_ERROR} {query.lastError().text()}")
            return success
        except Exception as e:
            print(f"{DATABASE_MESSAGE.DATABASE_VISION_DETAIL_FILE_INSERT_ERROR} {e}")
            return False
