"""
Main application file for the Shoe Database.
This application allows users to manage their shoe collection with CRUD (Create, Read, Update, and Delete) operations.
"""

# Import custom modules
from database import get_db_connection, close_db_connection
from auth import show_login_menu
from shoe_operations import show_shoe_menu

# Get database connection
conn, cur = get_db_connection()

def main():
    """Main entry point for the Shoe Database application."""
    # Bring up the login menu
    current_user_id = show_login_menu(cur, conn)
    
    # If the user successfully logs in, bring up the shoe menu
    if current_user_id is not None:
        show_shoe_menu(cur, conn, current_user_id)
    
    # Clean up database connections
    close_db_connection(conn, cur)


# A "guard" that only runs the main function if the script is executed directly
if __name__ == "__main__":
    main()