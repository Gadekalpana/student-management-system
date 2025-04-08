import os
import sqlite3

class Database:
    """Database manager for SQLite operations."""
    
    def __init__(self):
        """Initialize the database manager."""
        self.db_file = 'student_management.db'
        self.connection = None
    
    def get_connection(self):
        """Get a connection to the SQLite database."""
        self.connection = sqlite3.connect(self.db_file)
        return self.connection
    
    def close_connection(self):
        """Close the database connection."""
        if self.connection:
            self.connection.close()
    
    def create_tables(self):
        """Create necessary database tables if they don't exist."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Create students table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    roll_number TEXT UNIQUE NOT NULL,
                    name TEXT NOT NULL,
                    course TEXT NOT NULL,
                    gpa REAL NOT NULL
                )
            ''')
            
            conn.commit()
            conn.close()
            print("Database tables created successfully.")
        except Exception as e:
            print(f"Error creating database tables: {e}")

# Create a global database instance
db = Database()

def init_db(app):
    """Initialize the database for the application."""
    with app.app_context():
        db.create_tables()
