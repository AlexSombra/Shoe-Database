import psycopg2
import bcrypt
import os
import random
from getpass import getpass
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Connect to database
conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASS"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT")
)

cur = conn.cursor()

# Shoe database - 30+ shoes per brand
SHOE_DATABASE = {
    "Nike": [
        ("Air Force 1", ["White/White", "Black/Black", "Triple White", "Wheat", "Grey Fog"]),
        ("Dunk Low", ["Panda", "University Blue", "Kentucky", "Syracuse", "Coast"]),
        ("Air Max 90", ["Infrared", "Bacon", "Triple White", "Grey", "Black/White"]),
        ("Air Max 97", ["Silver Bullet", "Gold", "Triple Black", "Metallic Gold", "Navy"]),
        ("Air Max 1", ["Anniversary", "Patta Waves", "Crepe", "Safari", "Atmos Elephant"]),
        ("Blazer Mid", ["Vintage White", "Black Suede", "Navy", "Photon Dust", "Wheat"]),
        ("Cortez", ["White/Red", "Black/White", "Forest Green", "Leather White", "Navy"]),
        ("Air Max Plus", ["Hyper Blue", "Sunset", "Triple Black", "White/Blue", "Voltage Purple"]),
        ("React Vision", ["Gravity Purple", "Honeycomb", "Worldwide", "Triple White", "Black/Blue"]),
        ("Waffle One", ["Summit White", "Crater", "Sea Glass", "Light Armory Blue", "Black"]),
        ("Air Max 270", ["Triple Black", "White/Black", "Be True", "Throwback Future", "Bowfin"]),
        ("Pegasus 38", ["White/Blue", "Black/White", "Navy", "Florida State", "Barely Rose"]),
        ("Air Zoom Spiridon", ["Fossil", "Silver", "Black/Red", "Cage 2", "White/Blue"]),
        ("Air Tailwind 79", ["Sail/Blue", "Black/White", "Stranger Things", "OG", "Pink"]),
        ("Daybreak", ["Summit White", "Undercover Blue", "Black/White", "Peace", "Varsity Blue"]),
        ("LD Waffle", ["Pine Green", "Summit White", "Black Nylon", "Navy", "Grey"]),
        ("Air Presto", ["Triple White", "Off White", "USA", "Lightning", "Safari"]),
        ("Air Huarache", ["Triple White", "Scream Green", "DNA", "Purple Punch", "Black"]),
        ("Air Max 95", ["Neon", "Triple Black", "Grey/Orange", "Freddy Krueger", "Black/Volt"]),
        ("SB Dunk Low", ["Supreme Stars", "Travis Scott", "Raygun", "Staple Pigeon", "Heineken"]),
        ("Vapormax", ["Triple Black", "Be True", "Metallic Gold", "Navy", "White/Blue"]),
        ("Air Zoom GT Cut", ["Black", "White", "Team Red", "Blue", "Purple"]),
        ("Kobe 6", ["Grinch", "Mamba", "White/Del Sol", "All Star", "Chaos"]),
        ("LeBron 20", ["All Star", "Time Machine", "Bred", "Lakers", "Safari"]),
        ("KD 15", ["Aunt Pearl", "Easy Money", "White/Blue", "Black", "Sunset"]),
        ("Air Jordan Legacy 312", ["Storm Blue", "Black/Cement", "Chicago", "Lakers", "White"]),
        ("Shox TL", ["Black/Metallic", "White/Red", "Lime Green", "OG", "Triple Black"]),
        ("Joyride Run", ["Triple Black", "Platinum", "White/Red", "Blue", "Pink"]),
        ("ZoomX Vaporfly", ["Bright Mango", "Ekiden", "White/Blue", "Pink", "Black"]),
        ("Free Run 5.0", ["Black/White", "Triple White", "Grey", "Blue", "Triple Black"]),
        ("Revolution 6", ["Black/White", "Navy", "Grey", "Blue", "Red"]),
    ],
    "Jordan": [
        ("Air Jordan 1 High", ["Chicago", "Bred", "Royal", "Shadow", "Court Purple"]),
        ("Air Jordan 1 Low", ["Triple White", "Black Toe", "UNC", "Mystic Navy", "Panda"]),
        ("Air Jordan 3", ["White Cement", "Black Cement", "True Blue", "Fire Red", "Tinker"]),
        ("Air Jordan 4", ["Bred", "White Cement", "Fire Red", "Military Blue", "Thunder"]),
        ("Air Jordan 5", ["Fire Red", "Grape", "Michigan", "Metallic", "Off White Sail"]),
        ("Air Jordan 6", ["Carmine", "Infrared", "Black Infrared", "UNC", "Sport Blue"]),
        ("Air Jordan 11", ["Concord", "Space Jam", "Bred", "Legend Blue", "Cool Grey"]),
        ("Air Jordan 12", ["Flu Game", "Playoffs", "Cherry", "Dark Concord", "French Blue"]),
        ("Air Jordan 13", ["He Got Game", "Flint", "Playoffs", "Chicago", "Black Cat"]),
        ("Air Jordan 7", ["Raptor", "Bordeaux", "Cardinal", "Hare", "Olympic"]),
        ("Air Jordan 8", ["Aqua", "Playoffs", "Phoenix Suns", "Chrome", "South Beach"]),
        ("Air Jordan 9", ["UNC", "Dark Charcoal", "Black/Red", "City of Flight", "Change the World"]),
        ("Air Jordan 10", ["Chicago", "Steel", "Shadow", "Orlando", "Seattle"]),
        ("Air Jordan 14", ["Ferrari", "Black Toe", "Thunder", "Ginger", "Red Suede"]),
        ("Air Jordan Retro High OG", ["Seafoam", "Hyper Royal", "Heritage", "Dark Mocha", "Bio Hack"]),
        ("Air Jordan 1 Mid", ["Light Smoke Grey", "Chicago Toe", "Milan", "Lakers", "SE Black"]),
        ("Jordan Delta 2", ["Black/White", "Grey Fog", "Sail", "Barely Volt", "Navy"]),
        ("Jordan Max Aura 3", ["White/Black", "University Blue", "Black/Red", "Grey", "Navy"]),
        ("Jordan Zion 2", ["PF", "Melon Tint", "Multi-Color", "Black", "White"]),
        ("Jordan Luka 1", ["Bred", "White/Gold", "Photo Blue", "Black", "Sunset"]),
        ("Jordan 2x3", ["Black/White", "Red", "Blue", "Grey", "White"]),
        ("Air Jordan XXXVII", ["First Light", "Hare", "Championship", "Victory", "Low White"]),
        ("Air Jordan 36", ["Psychic Energy", "Guo Ailun", "Jayson Tatum", "First Light", "Black"]),
        ("Air Jordan 35", ["DNA", "Bayou Boys", "Warrior", "Morpho", "Bred"]),
        ("Why Not .6", ["Bright Concord", "Khelcey Barrs", "Pink", "Rattan", "White"]),
        ("Jordan Pro Strong", ["White/Black", "Black/Red", "Royal", "Grey", "Navy"]),
        ("Air Jordan 6 Rings", ["Black/White", "Championship", "Concord", "Cool Grey", "Bred"]),
        ("Jordan Jumpman 2021", ["Black/Metallic Gold", "White/Blue", "Red", "Grey", "Navy"]),
        ("Jordan Aerospace 720", ["Paris", "Bred", "White", "Black/Blue", "Metallic"]),
        ("Jordan Mars 270", ["Black/Anthracite", "Paris", "White", "Fire Red", "London"]),
        ("Air Jordan Future", ["Black", "Infrared", "Bred", "Cool Grey", "White"]),
    ],
    "Adidas": [
        ("Samba", ["Black/White", "Cloud White", "Navy", "Collegiate Green", "Burgundy"]),
        ("Campus 00s", ["Core Black", "Chalk White", "Grey", "Blue", "Green"]),
        ("Gazelle", ["Core Black", "Collegiate Navy", "Semi Pink", "Blue", "Grey"]),
        ("Superstar", ["White/Black", "Triple White", "All Black", "Floral", "Pride"]),
        ("Stan Smith", ["White/Green", "Triple White", "Primeknit", "Recon", "Lux"]),
        ("Ultraboost 22", ["Triple White", "Core Black", "Solar Red", "Navy", "Grey"]),
        ("NMD R1", ["Triple Black", "Japan Black", "Tri-Color", "White/Red", "Blue"]),
        ("Yeezy Boost 350 V2", ["Zebra", "Bred", "Cream White", "Blue Tint", "Beluga"]),
        ("Yeezy 500", ["Utility Black", "Blush", "Salt", "Super Moon Yellow", "Bone White"]),
        ("Yeezy Slide", ["Bone", "Pure", "Onyx", "Ochre", "Glow Green"]),
        ("Forum Low", ["White/Blue", "Bad Bunny Pink", "Cloud White", "Black/White", "Green"]),
        ("Forum Mid", ["White/Black", "Shock Pink", "Cloud White", "Blue", "Grey"]),
        ("Ozweego", ["Solar Yellow", "Clear Brown", "Core Black", "Cloud White", "Grey"]),
        ("Continental 80", ["White/Scarlet", "Off White", "Black", "Pride", "Aero Blue"]),
        ("ZX 2K Boost", ["Pure", "Grey", "Core Black", "Cloud White", "Navy"]),
        ("Nite Jogger", ["Core Black", "Crystal White", "Navy", "Grey Six", "Scarlet"]),
        ("Sobakov", ["White/Black", "Core Black", "Grey", "Blue", "Red"]),
        ("X_PLR", ["Core Black", "White", "Grey", "Navy", "Maroon"]),
        ("Swift Run", ["Core Black", "Cloud White", "Primeknit Grey", "Navy", "Pink"]),
        ("EQT Support", ["Core Black/Turbo", "Triple White", "Sub Green", "Grey", "Navy"]),
        ("Prophere", ["Core Black", "Cloud White", "Grey", "Solar Red", "Blue"]),
        ("Dame 8", ["Black/Solar", "White/Red", "Blue", "Halo Silver", "All Star"]),
        ("Harden Vol. 7", ["Black", "White", "Miami Nights", "Blue", "Red"]),
        ("Trae Young 2", ["Ice Trae", "Icee", "So So Def", "Blue", "White"]),
        ("D.O.N. Issue 4", ["Marvel", "Black/Gold", "White", "Blue", "Red"]),
        ("AE 1", ["White/Red", "New Wave", "Blue", "Black", "Velocity"]),
        ("Adizero Adios Pro 3", ["Solar Yellow", "Cloud White", "Core Black", "Blue", "Pink"]),
        ("4D Run 1.0", ["Core Black", "Cloud White", "Grey", "Solar Yellow", "Blue"]),
        ("Response CL", ["Core Black", "Cloud White", "Grey Three", "Navy", "Red"]),
        ("Retropy E5", ["Cloud White", "Core Black", "Grey", "Blue", "Purple"]),
        ("Dropset 2", ["Core Black", "Cloud White", "Grey", "Lucid Blue", "Red"]),
    ],
    "Puma": [
        ("Suede Classic", ["Black/White", "Peacoat", "Rhubarb", "High Risk Red", "Blue"]),
        ("RS-X", ["Toys White", "Reinvention", "Trophy", "Hard Drive", "Millenium"]),
        ("Clyde All-Pro", ["Team Gold", "Mid", "White/Black", "Red Blast", "Blue"]),
        ("MB.02", ["Red Blast", "Phenom", "Halo", "Slime", "Rick and Morty"]),
        ("Stewie 2", ["Sunset", "Lunar New Year", "Purple", "White/Gold", "Black"]),
        ("California", ["White/Black", "Premium", "Exotic", "OG", "Whisper White"]),
        ("Roma", ["White/Black", "Basic", "Classic", "Liberty", "OG"]),
        ("Thunder Spectra", ["Drizzle", "Puma Black", "Yellow", "Blue", "Grey"]),
        ("Cell Endura", ["Patent 98", "White/Black", "Animal Kingdom", "Blue", "Yellow"]),
        ("Mirage Sport", ["White/Navy", "Remix", "Tie Dye", "Triple White", "Black"]),
        ("Mayze", ["White/Black", "Classic", "Stacked", "Mix", "Chrome"]),
        ("Cali Sport", ["White/Pink", "Mix", "Heritage", "Black", "Navy"]),
        ("Future Rider", ["White/Blue", "Play On", "Chrome", "Black", "Purple"]),
        ("Easy Rider", ["White/Grey", "Vintage", "OG", "Black", "Navy"]),
        ("Rider FV", ["Sunset", "Chrome", "Black/Orange", "White", "Blue"]),
        ("Velocity Nitro 2", ["Black/Silver", "White/Blue", "Yellow", "Red", "Navy"]),
        ("Deviate Nitro 2", ["Blue", "Red", "White/Black", "Yellow", "Black"]),
        ("Magnify Nitro", ["Black/White", "Blue", "Red", "Grey", "Purple"]),
        ("Liberate Nitro", ["Yellow Alert", "Blue", "White/Red", "Black", "Orange"]),
        ("Fast-R Nitro Elite", ["Electric Peppermint", "Yellow", "White", "Blue", "Black"]),
        ("Blaze of Glory", ["Soft", "Sock", "OG", "Black/White", "Grey"]),
        ("Disc Blaze", ["Cell", "Leather", "Black/Red", "White", "Blue"]),
        ("Trinomic R698", ["Blocks", "White/Black", "Tech", "Blue", "Grey"]),
        ("XS 850", ["Primary", "Plus", "Black/White", "Navy", "Red"]),
        ("Ralph Sampson", ["Mid", "Lo", "White/Black", "Navy/White", "Grey"]),
        ("Slipstream", ["Lo", "Mid", "White/Blue", "Black/Red", "Triple White"]),
        ("Plexus", ["White/Blue", "Black", "Grey", "Navy", "Red"]),
        ("GV Special", ["Plus", "White/Navy", "Black", "Grey", "Red"]),
        ("Sky Modern", ["White/Black", "Blue", "Navy", "Grey", "Red"]),
        ("Palermo", ["White/Green", "Navy/Red", "Black", "Grey", "Blue"]),
        ("Mostro", ["Black", "White", "Navy", "Grey", "Red"]),
    ],
    "Under Armour": [
        ("Curry 10", ["White/Gold", "Candy Rain", "Team", "Black", "Session"]),
        ("Curry Flow 10", ["Birthday Drip", "Underrated", "White/Blue", "Black/Red", "Lime"]),
        ("Curry 9", ["International Women's Day", "Dub Nation", "White/Gold", "Black", "Blue"]),
        ("Havoc 4", ["White/Black", "Red/Black", "Blue", "Grey", "Team"]),
        ("Spawn 5", ["Black/Blue", "White/Red", "Team", "Purple", "Grey"]),
        ("HOVR Phantom 2", ["White", "Black", "Grey/Blue", "Navy", "Red"]),
        ("HOVR Sonic 5", ["White/Blue", "Black/Red", "Grey", "Navy/Orange", "Green"]),
        ("HOVR Machina 3", ["White/Black", "High-Vis Yellow", "Blue Circuit", "Red", "Grey"]),
        ("Flow Velociti Wind 2", ["White/Blue", "Black/Red", "High-Vis Yellow", "Grey", "Navy"]),
        ("SlipSpeed", ["White/Black", "Mega Magenta", "Black", "Lime", "Grey"]),
        ("TriBase Reign 5", ["Black/White", "Red/Black", "Blue", "Grey", "White"]),
        ("Project Rock 5", ["Black/White", "Blue", "Red", "Lime", "White/Grey"]),
        ("Project Rock 4", ["Stone/Black", "Castlerock", "Red/Black", "White", "Navy"]),
        ("Project Rock BSR 3", ["Black/White", "Lime/Black", "Red", "Blue", "Grey"]),
        ("Charged Assert 10", ["Black/White", "Grey", "Navy/Red", "Blue", "Triple Black"]),
        ("Charged Pursuit 3", ["Black", "White/Blue", "Grey/Red", "Navy", "Triple White"]),
        ("Surge 3", ["Black/White", "Grey", "Blue/Orange", "Red", "Navy"]),
        ("Micro G Valsetz", ["Black", "Coyote Brown", "Sage", "Triple Black", "Grey"]),
        ("Valsetz RTS 1.5", ["Black/Black", "Coyote", "Sage Green", "Storm", "Desert Sand"]),
        ("Stellar Tactical", ["Black", "Coyote Brown", "Burnt Orange", "Sage", "Grey"]),
        ("Anatomix Spawn", ["Low", "White/Red", "Black/Green", "Blue", "Team"]),
        ("Clutchfit Drive", ["Low", "White/Black", "Red", "Blue", "Team"]),
        ("Torch", ["White/Red", "Black/Blue", "Navy", "Grey", "Team"]),
        ("Lockdown 6", ["White/Black", "Black/Red", "Blue", "Navy", "Grey"]),
        ("Jet 23", ["White/Navy", "Black/Red", "Blue", "Grey", "Purple"]),
        ("Embiid 1", ["White/Gold", "Dark Matter", "Black/Red", "Blue", "Home"]),
        ("Grade School Assert", ["Black/Red", "White/Blue", "Grey", "Navy", "Purple"]),
        ("Assert 9", ["Black/White", "Grey/Orange", "Navy/Blue", "Red", "Triple Black"]),
        ("Remix", ["White/Black", "Blue", "Red", "Grey", "Navy"]),
        ("Ultimate Speed", ["Black/White", "Red/Black", "Blue", "Grey", "Navy"]),
        ("Magnetico Select", ["Black/White", "Red", "Blue", "Yellow", "Green"]),
    ]
}

CONDITIONS = ["New", "Like New", "Used"]
SIZES = [7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0, 10.5, 11.0, 11.5, 12.0, 12.5, 13.0]

def generate_shoe_data(brand, model, colorway):
    """Generate complete shoe data with random attributes"""
    size = random.choice(SIZES)
    condition = random.choice(CONDITIONS)
    
    # Generate price based on brand (rough estimates)
    base_prices = {
        "Nike": (80, 250),
        "Jordan": (150, 350),
        "Adidas": (70, 400),
        "Puma": (60, 180),
        "Under Armour": (70, 200)
    }
    
    min_price, max_price = base_prices.get(brand, (70, 200))
    price = round(random.uniform(min_price, max_price), 2)
    
    # Generate image filename
    image_name = f"{brand.lower().replace(' ', '_')}_{model.lower().replace(' ', '_')}_{colorway.lower().replace('/', '_').replace(' ', '_')}.jpg"
    
    return (brand, model, colorway, size, price, image_name, condition)

def pick_random_shoes(num_shoes=20, num_duplicates=2):
    """Pick random shoes ensuring at least num_duplicates sets of duplicates"""
    all_shoes = []
    
    # First, ensure we have at least num_duplicates sets of duplicates
    duplicate_shoes = []
    for _ in range(num_duplicates):
        brand = random.choice(list(SHOE_DATABASE.keys()))
        model, colorways = random.choice(SHOE_DATABASE[brand])
        colorway = random.choice(colorways)
        shoe_data = generate_shoe_data(brand, model, colorway)
        # Add this shoe twice
        duplicate_shoes.append(shoe_data)
        duplicate_shoes.append(shoe_data)
    
    # Now fill the rest with random unique shoes
    remaining_slots = num_shoes - (num_duplicates * 2)
    
    for _ in range(remaining_slots):
        brand = random.choice(list(SHOE_DATABASE.keys()))
        model, colorways = random.choice(SHOE_DATABASE[brand])
        colorway = random.choice(colorways)
        shoe_data = generate_shoe_data(brand, model, colorway)
        all_shoes.append(shoe_data)
    
    # Combine and shuffle
    all_shoes.extend(duplicate_shoes)
    random.shuffle(all_shoes)
    
    return all_shoes

# ==========================
# USER INPUT
# ==========================
print("=" * 60)
print("SHOE DATABASE - Random Collection Generator")
print("=" * 60)

username = input("\nEnter username for new test user: ").strip()
password = getpass("Enter password for new test user: ").strip()

if not username or not password:
    print("Error: Username and password cannot be empty!")
    cur.close()
    conn.close()
    exit(1)

print("\n" + "=" * 60)
print(f"Creating User: '{username}'")
print("=" * 60)

# Step 1: Clean up - Delete user if exists (and cascade delete shoes)
print("\n[1] Cleaning up existing test data...")
cur.execute("DELETE FROM shoes WHERE user_id IN (SELECT id FROM users WHERE username = %s)", (username,))
cur.execute("DELETE FROM users WHERE username = %s", (username,))
conn.commit()
print("[OK] Cleanup complete")

# Step 2: Create user with provided credentials
print(f"\n[2] Creating user '{username}'...")
email = f"{username}@test.com"
plain_password = password.encode("utf-8")
hashed_password = bcrypt.hashpw(plain_password, bcrypt.gensalt()).decode("utf-8")

cur.execute("INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s) RETURNING id", 
            (username, email, hashed_password))
user_id = cur.fetchone()[0]
conn.commit()
print(f"[OK] User created with ID: {user_id}")

# Step 3: Generate and add random shoes
print("\n[3] Generating 20 random shoes with at least 2 sets of duplicates...")
shoes_data = pick_random_shoes(num_shoes=20, num_duplicates=2)

print("[3] Adding shoes to collection...")
for i, shoe in enumerate(shoes_data, 1):
    brand, model, colorway, size, price, image, condition = shoe
    cur.execute(
        """
        INSERT INTO shoes (user_id, brand, model, colorway, size, price, image, condition)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (user_id, brand, model, colorway, size, price, image, condition)
    )
    print(f"  [{i}/20] Added: {brand} {model} - {colorway} (Size {size}, ${price}, {condition})")

conn.commit()
print("[OK] All 20 shoes added successfully")

# Step 4: Display summary statistics
print("\n[4] Collection Summary:")
print("-" * 60)

cur.execute("""
    SELECT brand, COUNT(*) as count
    FROM shoes
    WHERE user_id = %s
    GROUP BY brand
    ORDER BY count DESC
""", (user_id,))

brand_summary = cur.fetchall()
print("\nShoes by Brand:")
for brand, count in brand_summary:
    print(f"  • {brand}: {count} pairs")

cur.execute("""
    SELECT brand, model, COUNT(*) as count
    FROM shoes
    WHERE user_id = %s
    GROUP BY brand, model
    ORDER BY count DESC, brand, model
""", (user_id,))

model_summary = cur.fetchall()
print("\nShoes by Model (showing duplicates):")
for brand, model, count in model_summary:
    if count > 1:
        print(f"  • {brand} {model}: {count} pairs [DUPLICATE]")
    else:
        print(f"  • {brand} {model}: {count} pair")

cur.execute("""
    SELECT brand, model, colorway, size, price, condition
    FROM shoes
    WHERE user_id = %s
    ORDER BY brand, model, colorway
""", (user_id,))

all_shoes = cur.fetchall()
print("\nComplete Inventory:")
print("-" * 60)
for i, shoe in enumerate(all_shoes, 1):
    brand, model, colorway, size, price, condition = shoe
    print(f"{i:2d}. {brand:12s} | {model:25s} | {colorway:30s} | Size {size:4.1f} | ${price:6.2f} | {condition}")

print("\n" + "=" * 60)
print("TEST COMPLETED SUCCESSFULLY!")
print(f"User '{username}' can now login with password '{password}'")
print("=" * 60)

# Close connection
cur.close()
conn.close()
