"""
Input validation utilities for the Shoe Database application.
"""


def get_valid_float(prompt, min_value=None, max_value=None, allow_empty=False):
    """
    Prompt user for a valid float input with optional range validation.
    
    Args:
        prompt: The prompt message to display
        min_value: Optional minimum value (inclusive)
        max_value: Optional maximum value (inclusive)
        allow_empty: If True, allows empty input and returns None
        
    Returns:
        float: Valid float value within specified range, or None if empty and allowed
    """
    while True:
        user_input = input(prompt).strip()
        
        # Handle empty input
        if not user_input:
            if allow_empty:
                return None
            else:
                print("Error: Input cannot be empty. Please enter a number.")
                continue
        
        # Try to convert to float
        try:
            value = float(user_input)
        except ValueError:
            print(f"Error: '{user_input}' is not a valid number. Please try again.")
            continue
        
        # Validate range
        if min_value is not None and value < min_value:
            print(f"Error: Value must be at least {min_value}. Please try again.")
            continue
            
        if max_value is not None and value > max_value:
            print(f"Error: Value must be at most {max_value}. Please try again.")
            continue
        
        return value


def get_valid_string(prompt, min_length=1, max_length=None, allow_empty=False):
    """
    Prompt user for a valid string input with length validation.
    
    Args:
        prompt: The prompt message to display
        min_length: Minimum string length (default: 1)
        max_length: Optional maximum string length
        allow_empty: If True, allows empty input
        
    Returns:
        str: Valid string within specified length constraints
    """
    while True:
        user_input = input(prompt).strip()
        
        # Handle empty input
        if not user_input:
            if allow_empty:
                return ""
            else:
                print("Error: Input cannot be empty. Please try again.")
                continue
        
        # Validate length
        if len(user_input) < min_length:
            print(f"Error: Input must be at least {min_length} character(s). Please try again.")
            continue
            
        if max_length is not None and len(user_input) > max_length:
            print(f"Error: Input must be at most {max_length} character(s). Please try again.")
            continue
        
        return user_input


def get_valid_choice(prompt, valid_choices):
    """
    Prompt user for a choice from a list of valid options.
    
    Args:
        prompt: The prompt message to display
        valid_choices: List or set of valid choices (as strings)
        
    Returns:
        str: Valid choice selected by user
    """
    while True:
        user_input = input(prompt).strip()
        
        if user_input in valid_choices:
            return user_input
        else:
            print(f"Error: Invalid choice. Please select from: {', '.join(valid_choices)}")

def validate_email_format(email):
    """
    Basic email format validation.
    
    Args:
        email: Email string to validate
        
    Returns:
        bool: True if email format is valid, False otherwise
    """
    # Basic validation: contains @ and . after @
    if '@' not in email:
        return False
    
    local, domain = email.rsplit('@', 1)
    
    if not local or not domain:
        return False
        
    if '.' not in domain:
        return False
    
    return True


def get_valid_email(prompt):
    """
    Prompt user for a valid email address.
    
    Args:
        prompt: The prompt message to display
        
    Returns:
        str: Valid email address
    """
    while True:
        email = input(prompt).strip()
        
        if not email:
            print("Error: Email cannot be empty. Please try again.")
            continue
        
        if not validate_email_format(email):
            print("Error: Invalid email format. Please enter a valid email address.")
            continue
        
        return email

