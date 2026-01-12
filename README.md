# Shoe Database Application

A Python-based application for managing your personal shoe collection with user authentication and full CRUD operations.

## Features

- 🔐 User authentication (registration and login with bcrypt password hashing)
- 👟 Add, view, edit, and delete shoes from your collection
- 🔍 Advanced search and filtering by brand, model, colorway, size, and condition
- 📊 View inventory grouped by brand and model
- 🗄️ PostgreSQL database with automatic schema initialization

## Requirements

- Python 3.7+
- PostgreSQL 9.5+
- Dependencies listed in `requirements.txt`

## Installation

1. **Create and activate a virtual environment** (recommended to avoid global package installation):

   **Windows (PowerShell):**
   ```bash
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

   **Windows (Command Prompt):**
   ```bash
   python -m venv venv
   venv\Scripts\activate.bat
   ```

   **macOS/Linux:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

   You should see `(venv)` appear in your terminal prompt, indicating the virtual environment is active.

2. **Install Python dependencies** (inside the virtual environment):
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your database credentials:
```env
DB_NAME=your_database_name
DB_USER=your_username
DB_PASS=your_password
DB_HOST=localhost
DB_PORT=5432
```

4. Run the application (make sure your virtual environment is activated):
```bash
python app.py
```

The application will automatically create the necessary database tables on first run.

> **Note:** To deactivate the virtual environment when you're done, simply run `deactivate` in your terminal.

## Database Schema

The application uses two main tables:

### `users` Table
Stores user authentication information:
- `id` - Primary key (auto-increment)
- `username` - Unique username (max 50 characters)
- `email` - Unique email address (max 255 characters)
- `password_hash` - Bcrypt hashed password
- `created_at` - Account creation timestamp
- `last_login` - Last login timestamp

### `shoes` Table
Stores shoe inventory:
- `id` - Primary key (auto-increment)
- `user_id` - Foreign key to users (CASCADE DELETE)
- `brand` - Shoe brand name
- `model` - Shoe model name
- `colorway` - Color variant
- `size` - Shoe size (numeric)
- `price` - Purchase price (numeric)
- `image` - Image filename (optional)
- `condition` - Condition status (New, Used, Damaged, etc.)

**Index:** `shoes_user_brand_model_idx` on `(user_id, brand, model)` for optimized queries

## Manual Schema Setup

If you need to manually initialize the schema, you can run:

```bash
psql -U your_username -d your_database -f init_schema.sql
```

Or the schema will be automatically created when you run the application for the first time.

## Usage

1. **First Time Users**: Choose "New user" to create an account
2. **Existing Users**: Choose "Existing user" to login
3. **Manage Shoes**: Use the shoe menu to add, view, edit, or delete shoes from your collection

## Project Structure

- `app.py` - Main application entry point
- `database.py` - Database connection and schema initialization
- `auth.py` - User authentication (login/registration)
- `shoe_operations.py` - CRUD operations for shoes
- `validation.py` - Input validation utilities
- `init_schema.sql` - SQL schema definition for manual setup

## Notes

- All passwords are securely hashed using bcrypt
- Database connections are automatically managed
- Input validation prevents invalid data entry
- The application handles database errors gracefully
- **Always activate your virtual environment** before running the application or installing new packages
- The `venv` folder should not be committed to version control (add it to `.gitignore` if using Git)
