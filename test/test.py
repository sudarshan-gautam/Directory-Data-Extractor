import os
import tkinter as tk
from tkinter import filedialog, messagebox


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


# Function to process files
def process_files():
    base_dir = base_dir_var.get()
    output_file_path = output_file_path_var.get()

    if not base_dir or not output_file_path:
        messagebox.showerror("Error", "Please select both base directory and output file path.")
        return

    # Initialize counters
    total_characters = 0
    total_words = 0

    try:
        # Open the output file in write mode
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            # Traverse the project directory and count characters and words in each file
            for root, dirs, files in os.walk(base_dir):
                for file in files:
                    if file.endswith('.js') or file.endswith('.css') or file.endswith('.html') or file.endswith(
                            '.json') or file.endswith('.txt'):
                        file_path = os.path.join(root, file)
                        print(f"Processing {file_path}")
                        characters, words, content = count_in_file(file_path)
                        total_characters += characters
                        total_words += words

                        # Write the file path and content to the consolidated output file
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

        messagebox.showinfo("Success",
                            f"Processing completed.\nTotal characters: {total_characters}\nTotal words: {total_words}\nConsolidated file created at: {output_file_path}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


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

# Variables to hold the base directory and output file path
base_dir_var = tk.StringVar()
output_file_path_var = tk.StringVar()

# Create and place the widgets
frame = tk.Frame(root)
frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

tk.Label(frame, text="Base Directory:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
base_dir_entry = tk.Entry(frame, textvariable=base_dir_var, width=50)
base_dir_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
tk.Button(frame, text="Browse", command=select_base_dir).grid(row=0, column=2, padx=10, pady=10)

tk.Label(frame, text="Output File:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
output_file_entry = tk.Entry(frame, textvariable=output_file_path_var, width=50)
output_file_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
tk.Button(frame, text="Browse", command=select_output_file).grid(row=1, column=2, padx=10, pady=10)

tk.Button(frame, text="Process Files", command=process_files).grid(row=2, column=1, padx=10, pady=10)

# Bind the escape key to exit fullscreen mode
root.bind("<Escape>", exit_fullscreen)

# Make the entry fields expand with the window
frame.columnconfigure(1, weight=1)

# Run the application
root.mainloop()
