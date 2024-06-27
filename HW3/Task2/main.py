from pymongo import MongoClient
from bson.objectid import ObjectId
import sys

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client['cats_database']
collection = db['cats']

def display_all_records():
    """Display all records from the collection."""
    cats = collection.find()
    for cat in cats:
        print(cat)

def display_cat_by_name(name):
    """Display information about a cat by name."""
    cat = collection.find_one({"name": name})
    if cat:
        print(cat)
    else:
        print(f"No cat found with name: {name}")

def update_cat_age(name, new_age):
    """Update a cat's age by name."""
    result = collection.update_one({"name": name}, {"$set": {"age": new_age}})
    if result.matched_count:
        print(f"Updated age for {name} to {new_age}")
    else:
        print(f"No cat found with name: {name}")

def add_feature_to_cat(name, new_feature):
    """Add a new characteristic to the list of features of a cat by name."""
    result = collection.update_one({"name": name}, {"$addToSet": {"features": new_feature}})
    if result.matched_count:
        print(f"Added feature '{new_feature}' to {name}")
    else:
        print(f"No cat found with name: {name}")

def delete_cat_by_name(name):
    """Delete a record from the collection by the animal's name."""
    result = collection.delete_one({"name": name})
    if result.deleted_count:
        print(f"Deleted cat with name: {name}")
    else:
        print(f"No cat found with name: {name}")

def delete_all_records():
    """Delete all records from the collection."""
    result = collection.delete_many({})
    print(f"Deleted {result.deleted_count} records from the collection")

def create_sample_data():
    """Create sample data in the collection."""
    cats = [
        {"name": "barsik", "age": 3, "features": ["wears slippers", "allows to be petted", "ginger"]},
        {"name": "whiskers", "age": 5, "features": ["playful", "curious"]},
        {"name": "shadow", "age": 2, "features": ["quiet", "affectionate"]},
    ]
    collection.insert_many(cats)
    print("Sample data created.")

if __name__ == "__main__":
    # Create sample data for demonstration
    create_sample_data()

    # Menu for CRUD operations
    while True:
        print("\nChoose an operation:")
        print("1. Display all records")
        print("2. Display cat by name")
        print("3. Update cat age")
        print("4. Add feature to cat")
        print("5. Delete cat by name")
        print("6. Delete all records")
        print("7. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            display_all_records()
        elif choice == "2":
            name = input("Enter cat's name: ")
            display_cat_by_name(name)
        elif choice == "3":
            name = input("Enter cat's name: ")
            new_age = int(input("Enter new age: "))
            update_cat_age(name, new_age)
        elif choice == "4":
            name = input("Enter cat's name: ")
            new_feature = input("Enter new feature: ")
            add_feature_to_cat(name, new_feature)
        elif choice == "5":
            name = input("Enter cat's name: ")
            delete_cat_by_name(name)
        elif choice == "6":
            delete_all_records()
        elif choice == "7":
            sys.exit("Exiting...")
        else:
            print("Invalid choice. Please try again.")
