"""
Shoe operations module for the Shoe Database application.
Handles CRUD operations for shoes in the inventory.
"""

from validation import get_valid_float, get_valid_string
from psycopg2 import (
    DatabaseError,      # Base class for all database errors
    OperationalError,   # Connection issues, server problems
    IntegrityError,     # Constraint violations (unique, foreign key)
    DataError,          # Invalid data (wrong type, out of range)
    ProgrammingError    # SQL syntax errors, wrong table names
)


def select_shoe_from_inventory(cur, current_user_id):
    """
    Guide user through selecting a specific shoe from their inventory.
    Uses a drill-down approach: Brand → Model → Variant → Specific Shoe
    
    Args:
        cur: Database cursor object
        current_user_id: The ID of the current logged-in user
    
    Returns:
        tuple: (shoe_id, brand, model, colorway, size, price, image, condition) 
               or None if no shoes found or selection cancelled
    """
    # Step 1: Get all brands
    try:
        cur.execute("""
            SELECT brand, COUNT(*) AS quantity
            FROM shoes
            WHERE user_id = %s
            GROUP BY brand
            ORDER BY quantity DESC, brand ASC
            LIMIT 20;
        """, (current_user_id,))
        
        brand_results = cur.fetchall()
    except (OperationalError, ProgrammingError) as e:
        print(f"❌ Database error fetching brands: {e}")
        print("Unable to retrieve shoes. Please try again.")
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None
    
    if not brand_results:
        print("No shoes found in the database")
        return None
    
    # Step 2: Select a brand
    valid_selection = False
    while not valid_selection:
        print("\nHere are the brands of your shoes:")
        for brand, qty in brand_results:
            pair_word = "Pair" if qty == 1 else "Pairs"
            print(f"{brand}, {qty} {pair_word} of Shoes")
        
        brand_choice = input("\nSelect a brand: ")
        
        try:
            cur.execute("""
                SELECT model, COUNT(*) AS quantity
                FROM shoes
                WHERE user_id = %s AND brand = %s
                GROUP BY model
                ORDER BY quantity DESC, model ASC
                LIMIT 20;
            """, (current_user_id, brand_choice))
            
            model_results = cur.fetchall()
        except (OperationalError, ProgrammingError) as e:
            print(f"❌ Database error: {e}")
            print("Please try again.")
            continue
        
        if not model_results:
            print("\nError: Please select a valid brand")
        else:
            valid_selection = True
    
    # Step 3: Select a model
    valid_selection = False
    while not valid_selection:
        print("\nHere are the models of your shoes:")
        for model, qty in model_results:
            pair_word = "Pair" if qty == 1 else "Pairs"
            print(f"{model}, {qty} {pair_word} of Shoes")
        
        model_choice = input("\nSelect a model: ")
        
        try:
            cur.execute("""
                SELECT colorway, size, condition, COUNT(*) AS quantity
                FROM shoes
                WHERE user_id = %s
                    AND brand = %s
                    AND model = %s
                GROUP BY colorway, size, condition
                ORDER BY quantity DESC, colorway ASC, size ASC, condition ASC
                LIMIT 50;
            """, (current_user_id, brand_choice, model_choice))
            
            variant_results = cur.fetchall()
        except (OperationalError, ProgrammingError) as e:
            print(f"❌ Database error: {e}")
            print("Please try again.")
            continue
        
        if not variant_results:
            print("\nError: Please select a valid model")
        else:
            valid_selection = True
    
    # Step 4: Select a variant (colorway + size + condition)
    valid_selection = False
    while not valid_selection:
        i = 0
        print("\nHere are the variants of your shoes:")
        for colorway, size, condition, qty in variant_results:
            i += 1
            pair_word = "Pair" if qty == 1 else "Pairs"
            print(f"{i}. {model_choice}, {colorway}, {size}, {condition}, {qty} {pair_word} of Shoes")
        
        variant_choice = input("\nSelect a variant: ")
        if variant_choice.isdigit() and int(variant_choice) > 0 and int(variant_choice) <= i:
            valid_selection = True
        else:
            print("\nError: Please select a valid variant")
    
    # Step 5: Get the specific shoe record
    colorway_choice, size_choice, condition_choice, qty = variant_results[int(variant_choice) - 1]
    
    try:
        cur.execute("""
            SELECT id, brand, model, colorway, size, price, image, condition
            FROM shoes
            WHERE user_id = %s
                AND brand = %s
                AND model = %s
                AND colorway = %s
                AND size = %s
                AND condition = %s
            ORDER BY id ASC
            LIMIT 1;
        """, (current_user_id, brand_choice, model_choice, colorway_choice, size_choice, condition_choice))
        
        shoe_result = cur.fetchone()
    except (OperationalError, ProgrammingError) as e:
        print(f"❌ Database error fetching shoe details: {e}")
        print("Unable to retrieve shoe. Please try again.")
        return None
    
    if shoe_result is None:
        print("No shoe found with the given criteria")
        return None
    
    # Unpack and display the shoe details
    shoe_id, brand, model, colorway, size, price, image, condition = shoe_result
    image = image if image else "No image available"
    print(f"\nShoe Details: {brand}, {model}, {colorway}, {size}, ${price}, {image}, {condition}")
    print("\n")
    
    return (shoe_id, brand, model, colorway, size, price, image, condition)


def add_shoe(cur, conn, current_user_id):
    """
    Add a new shoe to the user's collection.
    
    Args:
        cur: Database cursor object
        conn: Database connection object for committing changes
        current_user_id: The ID of the current logged-in user
    """
    print("Adding a new shoe to your collection")
    
    # Validate string inputs
    brand = get_valid_string("Enter the brand of your shoe: ", min_length=1, max_length=100)
    model = get_valid_string("Enter the model of your shoe: ", min_length=1, max_length=100)
    colorway_choice = get_valid_string("Enter the colorway of your shoe: ", min_length=1, max_length=100)
    
    # Validate numeric inputs with proper ranges
    size = get_valid_float("Enter the size of your shoe: ", min_value=1.0, max_value=20.0)
    price = get_valid_float("Enter the price of your shoe: ", min_value=0.01, max_value=100000.0)
    
    # Optional image input
    image = get_valid_string(
        "Enter the image filename of your shoe(optional, but if you do make sure it's a .jpg, .jpeg, or .png file): ",
        allow_empty=True
    )
    
    # Validate condition input
    condition = get_valid_string("Enter the condition of your shoe(New, Used, Damaged, etc.): ", min_length=1, max_length=50)
    
    try:
        cur.execute(
            """
            INSERT INTO shoes (user_id, brand, model, colorway, size, price, image, condition)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (current_user_id, brand, model, colorway_choice, size, price, image or None, condition)
        )
        conn.commit()
        print("Shoe added to your collection!")
        
    except IntegrityError as e:
        conn.rollback()
        # Constraint violation - maybe a database constraint we don't know about
        print(f"❌ Database constraint error: Unable to add shoe")
        print("Please check your data and try again")
        
    except DataError as e:
        conn.rollback()
        # Invalid data type or out of range
        print(f"❌ Data error: {e}")
        print("Please check your input values")
        
    except OperationalError as e:
        conn.rollback()
        # Connection lost during operation
        print(f"❌ Database connection error")
        print("Please try again")
        
    except DatabaseError as e:
        conn.rollback()
        # Catch-all for other database errors
        print(f"❌ Database error occurred")
        print("The shoe was not added")
        
    except Exception as e:
        conn.rollback()
        print(f"❌ Unexpected error: {e}")


def view_all_shoes(cur, current_user_id):
    """
    Display all shoes in the user's collection grouped by brand and model.
    
    Args:
        cur: Database cursor object
        current_user_id: The ID of the current logged-in user
    """
    print("Grabbing all of your shoes from the database...")
    
    try:
        cur.execute(
            """
            SELECT brand, model, COUNT(*) AS quantity
            FROM shoes
            WHERE user_id = %s
            GROUP BY brand, model
            ORDER BY quantity DESC
            """,
            (current_user_id,)
        )
        shoes = cur.fetchall()
        
        print("\n brand | model | quantity\n")
        for shoe in shoes:
            print(shoe)
        print("\n")
        
    except OperationalError as e:
        print(f"❌ Database connection error")
        print("Unable to retrieve shoes. Please try again.")
        
    except ProgrammingError as e:
        print(f"❌ Query error")
        print("Unable to retrieve shoes")
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


def edit_shoe(cur, conn, shoe_data):
    """
    Edit attributes of a specific shoe.
    
    Args:
        cur: Database cursor object
        conn: Database connection object for committing changes
        shoe_data: Tuple containing shoe information from select_shoe_from_inventory
    """
    shoe_id, brand, model, colorway, size, price, image, condition = shoe_data
    
    print("Editing the shoe...")
    valid_selection = False
    while not valid_selection:
        print("What would you like to edit?")
        print("1. Brand\n2. Model\n3. Colorway\n4. Size\n5. Price\n6. Image\n7. Condition\n\n")
        edit_choice = input("Enter your choice: ")
        
        try:
            if edit_choice == "1":
                new_brand = get_valid_string("Enter the new brand name: ", min_length=1, max_length=100)
                cur.execute("UPDATE shoes SET brand = %s WHERE id = %s", (new_brand, shoe_id))
                conn.commit()
                print(f"Brand updated successfully to be '{new_brand}'")
                valid_selection = True
            elif edit_choice == "2":
                new_model = get_valid_string("Enter the new model name: ", min_length=1, max_length=100)
                cur.execute("UPDATE shoes SET model = %s WHERE id = %s", (new_model, shoe_id))
                conn.commit()
                print(f"Model updated successfully to be '{new_model}'")
                valid_selection = True
            elif edit_choice == "3":
                new_colorway = get_valid_string("Enter the new colorway: ", min_length=1, max_length=100)
                cur.execute("UPDATE shoes SET colorway = %s WHERE id = %s", (new_colorway, shoe_id))
                conn.commit()
                print(f"Colorway updated successfully to be '{new_colorway}'")
                valid_selection = True
            elif edit_choice == "4":
                new_size = get_valid_float("Enter the new size: ", min_value=1.0, max_value=20.0)
                cur.execute("UPDATE shoes SET size = %s WHERE id = %s", (new_size, shoe_id))
                conn.commit()
                print(f"Size updated successfully to be '{new_size}'")
                valid_selection = True
            elif edit_choice == "5":
                new_price = get_valid_float("Enter the new price: ", min_value=0.01, max_value=100000.0)
                cur.execute("UPDATE shoes SET price = %s WHERE id = %s", (new_price, shoe_id))
                conn.commit()
                print(f"Price updated successfully to be '{new_price}'")
                valid_selection = True
            elif edit_choice == "6":
                new_image = get_valid_string("Enter the new image filename: ", allow_empty=True)
                cur.execute("UPDATE shoes SET image = %s WHERE id = %s", (new_image or None, shoe_id))
                conn.commit()
                print(f"Image location updated successfully to be '{new_image}'")
                valid_selection = True
            elif edit_choice == "7":
                new_condition = get_valid_string("Enter the updated condition(New, Used, Damaged, etc.): ", min_length=1, max_length=50)
                cur.execute("UPDATE shoes SET condition = %s WHERE id = %s", (new_condition, shoe_id))
                conn.commit()
                print(f"Condition updated successfully to be '{new_condition}'")
                valid_selection = True
            else:
                print("\nError: Invalid choice, please try again")
                print(f"\nShoe Details: {brand}, {model}, {colorway}, {size}, ${price}, {image}, {condition}")
                print("\n")
                
        except IntegrityError as e:
            conn.rollback()
            print(f"❌ Database constraint error: Unable to update shoe")
            print("Please try again")
            
        except DataError as e:
            conn.rollback()
            print(f"❌ Data error: {e}")
            print("Please check your input values")
            
        except OperationalError as e:
            conn.rollback()
            print(f"❌ Database connection error")
            print("Please try again")
            
        except DatabaseError as e:
            conn.rollback()
            print(f"❌ Database error occurred")
            print("The shoe was not updated")
            
        except Exception as e:
            conn.rollback()
            print(f"❌ Unexpected error: {e}")


def delete_shoe(cur, conn, shoe_data):
    """
    Delete a specific shoe from the user's collection.
    
    Args:
        cur: Database cursor object
        conn: Database connection object for committing changes
        shoe_data: Tuple containing shoe information from select_shoe_from_inventory
    """
    shoe_id, brand, model = shoe_data[0], shoe_data[1], shoe_data[2]
    
    print("Deleting the shoe...")
    
    try:
        cur.execute("DELETE FROM shoes WHERE id = %s", (shoe_id,))
        conn.commit()
        print(f"{brand} {model} was deleted successfully")
        
    except IntegrityError as e:
        conn.rollback()
        print(f"❌ Database constraint error: Unable to delete shoe")
        print("Please try again")
        
    except OperationalError as e:
        conn.rollback()
        print(f"❌ Database connection error")
        print("Please try again")
        
    except DatabaseError as e:
        conn.rollback()
        print(f"❌ Database error occurred")
        print("The shoe was not deleted")
        
    except Exception as e:
        conn.rollback()
        print(f"❌ Unexpected error: {e}")


def show_shoe_menu(cur, conn, current_user_id):
    """
    Display and handle the main shoe management menu.
    
    Args:
        cur: Database cursor object
        conn: Database connection object
        current_user_id: The ID of the current logged-in user
    """
    shoe_menu_active = True
    
    while shoe_menu_active:
        print("Welcome to the Shoe Menu")
        print("1. Add a shoe")
        print("2. View all shoes")
        print("3. View a specific shoe")
        print("4. Edit a shoe")
        print("5. Delete a shoe")
        print("6. Exit")
        choice = input("Enter your choice: ")
        
        if choice == "1":
            add_shoe(cur, conn, current_user_id)
            
        elif choice == "2":
            view_all_shoes(cur, current_user_id)
            
        elif choice == "3":
            shoe_data = select_shoe_from_inventory(cur, current_user_id)
            if shoe_data is None:
                continue
                
        elif choice == "4":
            shoe_data = select_shoe_from_inventory(cur, current_user_id)
            if shoe_data is None:
                continue
            edit_shoe(cur, conn, shoe_data)
            
        elif choice == "5":
            shoe_data = select_shoe_from_inventory(cur, current_user_id)
            if shoe_data is None:
                continue
            delete_shoe(cur, conn, shoe_data)
            
        elif choice == "6":
            print("Exiting Shoe Menu...")
            shoe_menu_active = False
        else:
            print("\nError: Invalid choice, please try again\n")
