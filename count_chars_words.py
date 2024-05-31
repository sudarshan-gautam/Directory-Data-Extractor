import os
import sqlite3
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# Function to create or connect to the database
def create_db():
    conn = sqlite3.connect('processed_files.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY,
            filename TEXT,
            filepath TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Function to add a file to the database
def add_file_to_db(filename, filepath):
    conn = sqlite3.connect('processed_files.db')
    c = conn.cursor()
    c.execute('INSERT INTO files (filename, filepath) VALUES (?, ?)', (filename, filepath))
    conn.commit()
    conn.close()

# Function to get all files from the database
def get_files_from_db():
    conn = sqlite3.connect('processed_files.db')
    c = conn.cursor()
    c.execute('SELECT * FROM files')
    files = c.fetchall()
    conn.close()
    return files

# Function to delete a file from the database
def delete_file_from_db(file_id):
    conn = sqlite3.connect('processed_files.db')
    c = conn.cursor()
    c.execute('DELETE FROM files WHERE id = ?', (file_id,))
    conn.commit()
    conn.close()

# Function to count characters and words in a file
def count_in_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            characters = len(content)
            words = len(content.split())
            return characters, words, content
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return 0, 0, ''

# Function to open a file
def open_file(file_path):
    try:
        os.startfile(file_path)
    except Exception as e:
        messagebox.showerror("Error", f"Could not open file: {e}")

# Function to process files
def process_files():
    base_dir = base_dir_var.get()
    output_file_path = output_file_path_var.get()

    if not base_dir or not output_file_path:
        messagebox.showerror("Error", "Please select both base directory and output file path.")
        return

    try:
        # Open the output file in write mode
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            # Traverse the project directory and count characters and words in each file
            for root, dirs, files in os.walk(base_dir):
                for file in files:
                    if file.endswith('.js') or file.endswith('.css') or file.endswith('.html') or file.endswith('.json') or file.endswith('.txt'):
                        file_path = os.path.join(root, file)
                        characters, words, content = count_in_file(file_path)
                        output_file.write(f"======================\n")
                        output_file.write(f"File: {file_path}\n")
                        output_file.write(f"======================\n")
                        output_file.write(content + "\n\n")

            # Write the directory structure
            output_file.write("\nFile structure:\n\n")
            for dirpath, dirnames, filenames in os.walk(base_dir):
                level = dirpath.replace(base_dir, '').count(os.sep)
                indent = '│   ' * (level)
                output_file.write(f'{indent}├── {os.path.basename(dirpath)}/\n')
                subindent = '│   ' * (level + 1)
                for i, f in enumerate(filenames):
                    connector = '├── ' if i < len(filenames) - 1 else '└── '
                    output_file.write(f'{subindent}{connector}{f}\n')

        # Add the output file to the database
        add_file_to_db(os.path.basename(output_file_path), output_file_path)

        # Refresh the file list in the table
        refresh_file_list()

        messagebox.showinfo("Success", f"Processing completed.\nConsolidated file created at: {output_file_path}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Function to refresh the file list in the table
def refresh_file_list():
    for row in tree.get_children():
        tree.delete(row)
    for file in get_files_from_db():
        tree.insert("", "end", values=(file[0], file[1], file[2]))

# Function to select the base directory
def select_base_dir():
    dir_path = filedialog.askdirectory()
    base_dir_var.set(dir_path)

# Function to select the output file path
def select_output_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    output_file_path_var.set(file_path)

# Function to exit fullscreen mode
def exit_fullscreen(event=None):
    root.state('normal')

# Create the main application window
root = tk.Tk()
root.title("File Processor")

# Maximize the window to the screen size
root.state('zoomed')

# Create the database
create_db()

# Variables to hold the base directory and output file path
base_dir_var = tk.StringVar()
output_file_path_var = tk.StringVar()

# Create and place the widgets
top_frame = tk.Frame(root, bg='#1E5AAF', height=80)
top_frame.pack(side='top', fill='x')

title_label = tk.Label(top_frame, text="Directory Data Extractor", bg='#1E5AAF', fg='white', font=("Arial", 24, "bold"))
title_label.pack(pady=10)

main_frame = tk.Frame(root, bg='white')
main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

tk.Label(main_frame, text="Extract, Analyze, and Visualize Your Project Files", bg='white', fg='black', font=("Arial", 16)).pack(pady=(20, 10))
tk.Label(main_frame, text="☺", bg='white', fg='black', font=("Arial", 30)).pack()

input_frame = tk.Frame(main_frame, bg='white')
input_frame.pack(pady=(10, 20))

tk.Label(input_frame, text="Base Directory", bg='white', fg='black', font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10, sticky="e")
base_dir_entry = tk.Entry(input_frame, textvariable=base_dir_var, width=50, font=("Arial", 12))
base_dir_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
tk.Button(input_frame, text="Browse", command=select_base_dir, bg='#1E5AAF', fg='white', font=("Arial", 12)).grid(row=0, column=2, padx=10, pady=10)

tk.Label(input_frame, text="Output File", bg='white', fg='black', font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=10, sticky="e")
output_file_entry = tk.Entry(input_frame, textvariable=output_file_path_var, width=50, font=("Arial", 12))
output_file_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
tk.Button(input_frame, text="Browse", command=select_output_file, bg='#1E5AAF', fg='white', font=("Arial", 12)).grid(row=1, column=2, padx=10, pady=10)

tk.Button(main_frame, text="Process Files", command=process_files, bg='#1E5AAF', fg='white', font=("Arial", 12)).pack(pady=20)

# Create the table to display processed files
table_frame = tk.Frame(main_frame, bg='white')
table_frame.pack(expand=True, fill=tk.BOTH)

columns = ("ID", "Filename", "Filepath")
tree = ttk.Treeview(table_frame, columns=columns, show='headings', yscrollcommand=lambda f, l: scrollbar.set(f, l))

# Define headings
tree.heading("ID", text="ID")
tree.heading("Filename", text="Filename")
tree.heading("Filepath", text="Filepath")

# Define columns
tree.column("ID", anchor="w", width=50)
tree.column("Filename", anchor="w", width=200)
tree.column("Filepath", anchor="w", width=400)

# Add a scrollbar
scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=tree.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
tree.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

# Refresh the file list when the application starts
refresh_file_list()

# Define the function to open selected file
def on_open_button_click():
    selected_items = tree.selection()
    if not selected_items:
        messagebox.showerror("Error", "You have not selected a file to open!")
        return
    selected_item = selected_items[0]
    file_path = tree.item(selected_item, 'values')[2]
    open_file(file_path)

# Define the function to delete selected file
def on_delete_button_click():
    selected_items = tree.selection()
    if not selected_items:
        messagebox.showerror("Error", "You have not selected a file to delete!")
        return
    selected_item = selected_items[0]
    file_id = tree.item(selected_item, 'values')[0]
    delete_file_from_db(file_id)
    refresh_file_list()

# Add an "Open File" button
open_button = tk.Button(main_frame, text="Open File", command=on_open_button_click, bg='#1E5AAF', fg='white', font=("Arial", 12))
open_button.pack(pady=5)

# Add a "Delete File" button
delete_button = tk.Button(main_frame, text="Delete File", command=on_delete_button_click, bg='#1E5AAF', fg='white', font=("Arial", 12))
delete_button.pack(pady=5)

bottom_frame = tk.Frame(root, bg='#1E5AAF', height=40)
bottom_frame.pack(side='bottom', fill='x')

footer_label = tk.Label(bottom_frame, text="Copyright © Developed By Sudarshan Gautam", bg='#1E5AAF', fg='white', font=("Arial", 10))
footer_label.pack(pady=10)

# Bind the escape key to exit fullscreen mode
root.bind("<Escape>", exit_fullscreen)

# Make the entry fields expand with the window
input_frame.columnconfigure(1, weight=1)

# Run the application
root.mainloop()
