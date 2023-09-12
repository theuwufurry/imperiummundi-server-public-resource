import os
import json
import random
import tkinter as tk
from tkinter import simpledialog, messagebox

# Function to get user input
def get_input(prompt, default=""):
    user_input = simpledialog.askstring("Input", prompt, initialvalue=default)
    return user_input

# Function to generate a random number not in ferretsarecute.json
def generate_unique_random_number(existing_numbers, max_value):
    while True:
        random_num = random.randint(0, max_value)
        if random_num not in existing_numbers:
            return random_num

# Function to create or update the dog.json file
def create_or_update_dog_json(dog_name, directory):
    dog_json_path = os.path.join(directory, f"{dog_name}.json")

    if os.path.exists(dog_json_path):
        with open(dog_json_path, "r") as dog_json_file:
            dog_data = json.load(dog_json_file)
    else:
        dog_data = {
            "parent": "item/handheld",
            "textures": {
                "layer0": f"item/{dog_name}"  # Set "layer0" to user input
            },
            "overrides": []
        }

    with open(dog_json_path, "w") as dog_json_file:
        json.dump(dog_data, dog_json_file, indent=4)

    messagebox.showinfo("JSON Generated", f'JSON file "{dog_name}.json" has been created/updated for the dog in the directory: {directory}')

# Function to handle the item creation process
def create_items():
    while True:
        cat_name = get_input("Enter the name for the cat item (e.g., cat):")
        if not cat_name:
            break

        ant_name = get_input("Enter the name for the ant (e.g., ant):")
        if not ant_name:
            break

        directory = "C:\\Users\\funboy\\Documents\\resoursepacks\\resourcepacks\\imperiummundi-server-public-resource\\assets\\minecraft\\models\\item"

        # Create item JSON for the cat
        item_data = {
            "parent": f"item/itemmodels/{ant_name}",
            "textures": {
                "layer0": f"item/{cat_name}"
            }
        }
        item_filename = f"{cat_name}.json"
        item_dir = os.path.join(directory, "ferrets")
        os.makedirs(item_dir, exist_ok=True)
        item_path = os.path.join(item_dir, item_filename)
        with open(item_path, "w") as json_file:
            json.dump(item_data, json_file, indent=4)
        messagebox.showinfo("JSON Generated", f'JSON file "{item_filename}" has been created for the item in the directory: {item_dir}')

        dog_name = get_input("Enter the name for the dog item (e.g., dog):")
        if not dog_name:
            break

        # Create or update dog.json based on user input
        create_or_update_dog_json(dog_name, directory)

        twenty = generate_unique_random_number([], 104230)
        ferretsarecute_path = os.path.join(directory, "ferretsarecute.json")

        try:
            if os.path.exists(ferretsarecute_path):
                with open(ferretsarecute_path, "r") as ferretsarecute_file:
                    existing_data = json.load(ferretsarecute_file)
            else:
                existing_data = {}
        except json.JSONDecodeError:
            existing_data = {}

        while str(twenty) in existing_data:
            twenty = generate_unique_random_number(existing_data, 104230)

        # Add predicate to dog.json
        predicate_data = {
            "model": cat_name
        }
        dog_json_path = os.path.join(directory, f"{dog_name}.json")
        add_predicate_to_json(dog_json_path, predicate_data, cat_name, twenty)

        # Update ferretsarecute.json
        existing_data[str(twenty)] = cat_name
        with open(ferretsarecute_path, "w") as ferretsarecute_file:
            json.dump(existing_data, ferretsarecute_file, indent=4)

        messagebox.showinfo("JSON Updated", f'JSON files have been created/updated for the items in the directory: {directory}')

# Function to add a predicate to an existing JSON file
def add_predicate_to_json(json_path, predicate_data, cat_name, twenty):
    if os.path.exists(json_path):
        with open(json_path, "r") as existing_json_file:
            existing_data = json.load(existing_json_file)

        if "overrides" in existing_data:
            new_json_data = {
                "predicate": {
                    "custom_model_data": twenty
                },
                "model": f"item/ferrets/{cat_name}"
            }
            existing_data["overrides"].append(new_json_data)

            with open(json_path, "w") as updated_json_file:
                json.dump(existing_data, updated_json_file, indent=4)
            messagebox.showinfo("JSON Updated", f'JSON file "{os.path.basename(json_path)}" has been updated.')
        else:
            messagebox.showerror("Error", f'The JSON file "{os.path.basename(json_path)}" does not have an "overrides" section.')
    else:
        messagebox.showerror("Error", f'The JSON file "{os.path.basename(json_path)}" does not exist.')

# Create a GUI window
root = tk.Tk()
root.withdraw()  # Hide the main GUI window

# Call the create_items function to start the item creation process
create_items()

# Close the GUI window
root.destroy()
