#import the tkinter library
import tkinter as tk
#Import filedialog
from tkinter import filedialog, messagebox
import os

# Initialize the main windows
root = tk.Tk()
#set the windows title
root.title("File Renamer Script")
root.geometry("400x300")

#defining the folder_lable
folder_label = tk.Label(root, width=50, text="Folder Path: ")
folder_label.pack(pady=5)
#defining the folder_entry
folder_entry = tk.Entry(root, width=50) 
folder_entry.pack(pady=5)

#function to browse and select folder
def browse_folder():
    folder_path = filedialog.askdirectory()
    folder_entry.delete(0, tk.END)
    folder_entry.insert(0, folder_path)

#Browse button for folder path
browse_button = tk.Button(root, text="Browse", command=browse_folder)
browse_button.pack(pady=5)

#the new name prefix label and entry
new_name_label = tk.Label(root, text= "New Name prefix:")
new_name_label.pack(pady=5)
new_name_entry = tk.Entry(root, width=50)
new_name_entry.pack(pady=5)

# Function to rename files
def rename_files():
    folder_path = folder_entry.get()
    name_prefix = new_name_entry.get()

    #validate input
    if not folder_path or not os.path.isdir(folder_path):
        messagebox.showerror("Error", "Plese Select a Valid Folder.")
        return
    if not name_prefix:
        messagebox.showerror("Error", "please Enter a Valid Name Prefix.")
        return

    #Rename files in the folder
# Rename files in the folder
try:
    for count, filename in enumerate(os.listdir(folder_path), start=1):
        file_extension = os.path.splitext(filename)[1]  # Get file extension
        new_name = f"{name_prefix}_{count}{file_extension}"  # Corrected line

        src = os.path.join(folder_path, filename)
        dst = os.path.join(folder_path, new_name)
        os.rename(src, dst)
    messagebox.showinfo("Success", "Files have been renamed successfully!")
except Exception as e:
    messagebox.showerror("Error", f"An error occurred: {e}")


rename_button = tk.Button(root, text="Rename Files", command=rename_files )
rename_button.pack(pady=20)



#Run the main event
root.mainloop()
