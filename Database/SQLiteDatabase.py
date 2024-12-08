import sqlite3
from typing import List, Tuple, Any, Optional


class SQLiteDatabase:
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        print(f"Connected to database: {db_name}")

    def create_table(self, table_name: str, columns: str) -> None:
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})"
        self.cursor.execute(query)
        self.conn.commit()
        print(f"Table '{table_name}' created (if not exists).")

    def insert(self, table_name: str, columns: str, values: Tuple) -> None:
        placeholders = ', '.join(['?'] * len(values))
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        self.cursor.execute(query, values)
        self.conn.commit()
        print(f"Inserted record into '{table_name}'.")

    def fetch_all(self, table_name: str) -> List[Tuple]:
        query = f"SELECT * FROM {table_name}"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def fetch_one(self, table_name: str, condition: str, params: Tuple = ()) -> Optional[Tuple]:
        query = f"SELECT * FROM {table_name} WHERE {condition} LIMIT 1"
        self.cursor.execute(query, params)
        return self.cursor.fetchone()

    def update_by_id(self, table_name: str, id_column: str, record_id: Any, update_values: dict) -> None:
        set_clause = ', '.join([f"{column} = ?" for column in update_values.keys()])
        query = f"UPDATE {table_name} SET {set_clause} WHERE {id_column} = ?"
        params = tuple(update_values.values()) + (record_id,)
        self.cursor.execute(query, params)
        self.conn.commit()
        print(f"Updated record with ID {record_id} in '{table_name}'.")

    def delete(self, table_name: str, condition: str, params: Tuple) -> None:
        query = f"DELETE FROM {table_name} WHERE {condition}"
        self.cursor.execute(query, params)
        self.conn.commit()
        print(f"Deleted record(s) from '{table_name}'.")

    def drop_table(self, table_name: str) -> None:
        query = f"DROP TABLE IF EXISTS {table_name}"
        self.cursor.execute(query)
        self.conn.commit()
        print(f"Table '{table_name}' dropped.")

    def close(self) -> None:
        self.conn.close()
        print(f"Closed connection to database: {self.db_name}")