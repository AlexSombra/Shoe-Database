"""
Authentication module for the Shoe Database application.
Handles user registration, login, and validation.
"""

import bcrypt
from getpass import getpass
from validation import get_valid_email
from psycopg2 import (
    DatabaseError,      # Base class for all database errors
    OperationalError,   # Connection issues, server problems
    IntegrityError,     # Constraint violations (unique, foreign key)
    DataError,          # Invalid data (wrong type, out of range)
    ProgrammingError    # SQL syntax errors, wrong table names
)


def login_user(cur):
    """
    Handle user login by prompting for credentials and validating against database.
    
    Args:
        cur: Database cursor object
        
    Returns:
        int: User ID of the logged-in user
    """
    not_logged_in = True
    while not_logged_in:
        username = input("Enter your username: ")
        password = getpass("Enter your password: ")
        
        try:
            # Fetch stored password hash for this username
            cur.execute("SELECT id, password_hash FROM users WHERE username = %s", (username,))
            row = cur.fetchone()
            
            if row is None:
                print("Invalid username or password, please try again")
                continue
                
            user_id_from_db = row[0]
            stored_hash = row[1]
            
            # Compare entered password against stored hash
            if bcrypt.checkpw(password.encode("utf-8"), stored_hash.encode("utf-8")):
                print("Login successful, heading to main menu...")
                not_logged_in = False
                return user_id_from_db
            else:
                print("Invalid username or password, please try again")
                
        except OperationalError as e:
            print(f"❌ Database connection error: {e}")
            print("Unable to login. Please try again.")
            continue
            
        except ProgrammingError as e:
            print(f"❌ Query error: {e}")
            print("Unable to login. Please try again.")
            continue
            
        except Exception as e:
            print(f"❌ Unexpected error during login: {e}")
            print("Please try again.")
            continue


def create_account(cur, conn):
    """
    Handle new user account creation with validation.
    
    Args:
        cur: Database cursor object
        conn: Database connection object for committing changes
        
    Returns:
        int or None: User ID of the newly created user after successful login, or None on error
    """
    print("New user, you will need to create an account")
    
    # Validate unique username
    username = input("Enter your username: ")
    try:
        cur.execute("SELECT 1 FROM users WHERE username = %s", (username,))
        exists = cur.fetchone() is not None
    except (OperationalError, ProgrammingError) as e:
        print(f"❌ Database error checking username: {e}")
        print("Unable to create account. Please try again later.")
        return None
    
    while exists:
        print("Username already exists, please choose a different username")
        username = input("Enter your username: ")
        try:
            cur.execute("SELECT 1 FROM users WHERE username = %s", (username,))
            exists = cur.fetchone() is not None
        except (OperationalError, ProgrammingError) as e:
            print(f"❌ Database error checking username: {e}")
            print("Unable to create account. Please try again later.")
            return None
    
    # Validate unique email
    email = get_valid_email("Enter your email: ")
    try:
        cur.execute("SELECT 1 FROM users WHERE email = %s", (email,))
        exists = cur.fetchone() is not None
    except (OperationalError, ProgrammingError) as e:
        print(f"❌ Database error checking email: {e}")
        print("Unable to create account. Please try again later.")
        return None
    
    while exists:
        print("Email already exists, please choose a different email")
        email = get_valid_email("Enter your email: ")
        try:
            cur.execute("SELECT 1 FROM users WHERE email = %s", (email,))
            exists = cur.fetchone() is not None
        except (OperationalError, ProgrammingError) as e:
            print(f"❌ Database error checking email: {e}")
            print("Unable to create account. Please try again later.")
            return None
    
    # Hash password and create user
    plain_password = getpass("Enter your password: ").encode("utf-8")
    hashed_password = bcrypt.hashpw(plain_password, bcrypt.gensalt()).decode("utf-8")
    
    try:
        cur.execute(
            "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
            (username, email, hashed_password)
        )
        conn.commit()
        print("User created successfully, redirecting to login...")
        return login_user(cur)
        
    except IntegrityError as e:
        conn.rollback()
        # This shouldn't happen since we validate uniqueness first
        # But handle it anyway in case of race condition
        print("❌ Error: Username or email already exists")
        print("Please try again with different credentials")
        return None
        
    except OperationalError as e:
        conn.rollback()
        print("❌ Database connection error")
        print("Unable to create account. Please try again later.")
        return None
        
    except DataError as e:
        conn.rollback()
        print(f"❌ Data error: {e}")
        print("Please check your input values")
        return None
        
    except Exception as e:
        conn.rollback()
        print(f"❌ Unexpected error creating account")
        print("Please try again")
        return None


def show_login_menu(cur, conn):
    """
    Display login menu and handle user choice for account creation or login.
    
    Args:
        cur: Database cursor object
        conn: Database connection object
        
    Returns:
        int or None: User ID if successfully logged in, None if user chose to exit
    """
    login_menu_active = True
    current_user_id = None
    
    while login_menu_active:
        print("Welcome to the Shoe Database")
        print("Are you a new user or an existing user?")
        print("1. New user")
        print("2. Existing user")
        print("3. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            current_user_id = create_account(cur, conn)
            login_menu_active = False
        elif choice == "2":
            print("Existing user, redirecting to login")
            current_user_id = login_user(cur)
            login_menu_active = False
        elif choice == "3":
            print("Exiting Shoe Database...")
            login_menu_active = False
        else:
            print("\nError: Invalid choice, please try again\n")
    
    return current_user_id
