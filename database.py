import sqlite3

class Database:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        print("Database connection established.")
        self.setup_database()

    def execute_query(self, query, params=None):
        try:
            self.cursor.execute(query, params if params else ())
            self.connection.commit()
            print("Query executed successfully.")
        except sqlite3.Error as e:
            print(f"Error executing query: {e}")

    def fetch_data(self, query, params=None):
        try:
            self.cursor.execute(query, params if params else ())
            data = self.cursor.fetchall()
            print("Data fetched successfully:", data)
            return data
        except sqlite3.Error as e:
            print(f"Error fetching data: {e}")
            return None

    def close_connection(self):
        self.cursor.close()
        self.connection.close()
        print("Database connection closed.")

    def setup_database(self):
        """Create tables if they don't exist."""
        create_users_table = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        );
        """
        create_transactions_table = """
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            amount REAL,
            category TEXT,
            type TEXT,
            note TEXT,
            date TEXT
        );
        """
        create_categories_table = """
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE
        );
        """
        self.execute_query(create_users_table)
        self.execute_query(create_transactions_table)
        self.execute_query(create_categories_table)
        try:
            self.execute_query("ALTER TABLE transactions ADD COLUMN type TEXT;")
            self.execute_query("ALTER TABLE transactions ADD COLUMN note TEXT;")
            print("Column 'type' added to 'transactions' table.")
        except sqlite3.OperationalError as e:
            print("Column 'type' already exists in 'transactions' table or other error:", e)
