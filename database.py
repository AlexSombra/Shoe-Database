"""
Database connection module for the Shoe Database application.
"""

import psycopg2
from psycopg2 import OperationalError, DatabaseError   # Connection issues, server problems
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def initialize_schema(conn, cur):
    """
    Initialize the database schema by creating necessary tables and indexes.
    This function is idempotent - it can be run multiple times safely.
    
    Args:
        conn: Database connection object
        cur: Database cursor object
        
    Returns:
        bool: True if schema initialization was successful, False otherwise
    """
    try:
        # Create users table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                last_login TIMESTAMPTZ
            );
        """)
        
        # Create shoes table with foreign key cascade
        cur.execute("""
            CREATE TABLE IF NOT EXISTS shoes (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                brand TEXT NOT NULL,
                model TEXT NOT NULL,
                colorway TEXT NOT NULL,
                size DOUBLE PRECISION NOT NULL,
                price DOUBLE PRECISION NOT NULL,
                image TEXT,
                condition TEXT NOT NULL
            );
        """)
        
        # Create index for better query performance
        # Use CREATE INDEX IF NOT EXISTS (PostgreSQL 9.5+)
        cur.execute("""
            CREATE INDEX IF NOT EXISTS shoes_user_brand_model_idx
            ON shoes (user_id, brand, model);
        """)
        
        conn.commit()
        print("✓ Database schema initialized successfully")
        return True
        
    except DatabaseError as e:
        conn.rollback()
        print(f"❌ Error initializing database schema: {e}")
        print("Please check your database permissions and try again.")
        return False
        
    except Exception as e:
        conn.rollback()
        print(f"❌ Unexpected error during schema initialization: {e}")
        return False


def get_db_connection():
    """
    Establish and return a connection to the PostgreSQL database.
    Automatically initializes the database schema if tables don't exist.
    
    Returns:
        tuple: (connection, cursor) objects for database operations
        
    Raises:
        SystemExit: If connection fails (exits the program)
    """
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
        cur = conn.cursor()
        
        # Initialize schema (create tables and indexes if they don't exist)
        schema_initialized = initialize_schema(conn, cur)
        if not schema_initialized:
            print("⚠️  Warning: Schema initialization encountered issues")
            print("The application may not work correctly")
        
        return conn, cur
        
    except OperationalError as e:
        # Connection failed - server down, wrong credentials, etc.
        print(f"❌ Cannot connect to database: {e}")
        print("\nPlease check:")
        print("  - Database server is running")
        print("  - Credentials in .env file are correct")
        print("  - Network connection is available")
        exit(1)  # Exit because app can't function without DB
    except Exception as e:
        print(f"❌ Unexpected error connecting to database: {e}")
        exit(1)


def close_db_connection(conn, cur):
    """
    Safely close database connection and cursor.
    
    Args:
        conn: Database connection object
        cur: Database cursor object
    """
    if cur:
        cur.close()
    if conn:
        conn.close()
    print("Database connection closed successfully.")
