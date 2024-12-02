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
        query = f"SELECT * FROM {table_name} WHERE {condition}"  
        self.cursor.execute(query, params)
        return self.cursor.fetchone()

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

    def update_page_history(self, username: str, page_index: int) -> None:
        # Fetch current history
        record = self.fetch_one("page_history", "username = ?", (username,))
        if record:
            # Update existing history
            current_history = record[2]  
            updated_history = f"{current_history},{page_index}"
            query = "UPDATE page_history SET page_history = ? WHERE username = ?"
            self.cursor.execute(query, (updated_history, username))
        else:
            # Insert new history
            self.insert("page_history", "username, page_history", (username, str(page_index)))
        self.conn.commit()
        print(f"Updated page history for user '{username}'.")

    def get_last_page(self, username: str) -> int:
        record = self.fetch_one("page_history", "username = ?", (username,))
        if record and record[2]:
            page_history = record[2].split(",")  # Split the history string
            return int(page_history[-1])  # Get the last page index
        return 0  # Default to page index 0 if no history exists

    def drop_all_tables(self, confirm=True):
        if confirm:
            proceed = input("Are you sure you want to clear all tables? (yes/no): ").lower()
            if proceed != "yes":
                print("Operation canceled.")
                return

        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
        tables = self.cursor.fetchall()

        for table_name in tables:
            self.drop_table(table_name[0])  
        print("Dropped all user-defined tables from the database.")


def initialize_database():
    db = SQLiteDatabase("Data/Database.db")

    # Drop all tables at startup 
    db.drop_all_tables(confirm=False)  # Will delete this line of code in future (using to test features)

    # Create current_user table
    db.create_table(
        "current_user", 
        "id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT"
    )

    # Create page_history table
    db.create_table(
        "page_history",
        "id INTEGER PRIMARY KEY AUTOINCREMENT, page TEXT"
    )

    return db



