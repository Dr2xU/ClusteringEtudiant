import random
from datetime import datetime

existing_ids = set()

def load_existing_ids(id_list):
    """Call this to populate existing IDs from file or database."""
    global existing_ids
    existing_ids = set(id_list)

def generate_unique_id():
    """Generates a 10-digit unique ID: YYYY + 6 random digits."""
    current_year = datetime.now().year
    while True:
        random_part = random.randint(100000, 999999)
        new_id = f"{current_year}{random_part}"
        if new_id not in existing_ids:
            existing_ids.add(new_id)
            return new_id
