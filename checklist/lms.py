import customtkinter as ctk
import sqlite3
from tkinter import messagebox
from PIL import Image, ImageTk

# Function to create the database table
def create_table():
    conn = sqlite3.connect('clothes.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clothes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT NOT NULL,
            quantity INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Function to add multiple records to the database
def add_records(records):
    conn = sqlite3.connect('clothes.db')
    cursor = conn.cursor()
    for item_name, quantity in records:
        if quantity.isdigit() and int(quantity) > 0:  # Only add if quantity is greater than 0
            cursor.execute('INSERT INTO clothes (item_name, quantity) VALUES (?, ?)', (item_name, int(quantity)))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "All records added successfully!")

# Function to handle submission of all inputs
def submit_all():
    records_to_add = [(item, entry.get()) for item, entry in item_entries.items()]
    add_records(records_to_add)

# CustomTkinter Setup
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# GUI Setup
root = ctk.CTk()
root.title("Clothes Checklist")
root.geometry("600x800")  # Adjusted height to fit the image

# Main frame configuration to simulate rounded corners
main_frame = ctk.CTkFrame(root, corner_radius=15, fg_color="#718690")
main_frame.pack(padx=20, pady=20, fill="both", expand=True)

# Title label
title_label = ctk.CTkLabel(main_frame, text="CHECKLIST", font=ctk.CTkFont(size=30, weight="bold"))
title_label.pack(pady=20)

# Load and display the image
try:
    image = Image.open("Figma basics.png")  # Replace with the name of your image file
    image = image.resize((150, 150), Image.ANTIALIAS)  # Resize as needed
    img = ImageTk.PhotoImage(image)

    image_label = ctk.CTkLabel(main_frame, image=img, text="")
    image_label.pack(pady=10)
except FileNotFoundError:
    print("Image file not found. Please ensure the image file is in the correct directory.")

# Frame for the checklist with rounded corners
checklist_frame = ctk.CTkFrame(main_frame, corner_radius=15, fg_color="#8B9EA8")
checklist_frame.pack(padx=20, pady=10, fill="both", expand=True)

# Items and their corresponding entry widgets
items = ["Shirt", "T shirt", "Lower", "Jeans", "Shorts", "Dupatta", "Bedsheet", "Pillow cover", "Blanket", "Kurta"]
item_entries = {}

# Create labels and dropdowns for each item
for i, item in enumerate(items):
    ctk.CTkLabel(checklist_frame, text=item, font=ctk.CTkFont(size=14)).grid(row=i, column=0, padx=10, pady=5, sticky='w')
    item_var = ctk.StringVar(value='0')
    dropdown = ctk.CTkComboBox(checklist_frame, variable=item_var, values=[str(x) for x in range(0, 21)], width=60)
    dropdown.grid(row=i, column=1, padx=10, pady=5)
    item_entries[item] = item_var

# Submit button
submit_button = ctk.CTkButton(main_frame, text="Submit", command=submit_all, fg_color="#5E6F78", font=ctk.CTkFont(size=14, weight="bold"))
submit_button.pack(pady=20)

# Initialize database
create_table()

# Start the main event loop
root.mainloop()

