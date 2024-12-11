import tkinter
from tkinter import Tk, Label, Button, filedialog
import os
from tkinter.messagebox import showerror, showinfo
from converter import convert_doc_to_pdf

def run_converter():
    """
    Handles file selection and conversion process.
    Opens dialogs for selecting the input .docx file and saving the output .pdf file.
    """
    try:
        # Open file dialog to select the input .docx file
        input_path = filedialog.askopenfilename(filetypes=[("Word Documents", "*.docx")])
        if not input_path:  # If the user cancels file selection
            return

        # Open file dialog to specify the output .pdf file
        output_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
        if not output_path:  # If the user cancels save-as dialog
            return

        # Call the convert function
        success, message = convert_doc_to_pdf(input_path, output_path)
        if success:
            showinfo("Success", message)  # Show success message
        else:
            showerror("Error", message)  # Show error message
    except Exception as e:
        # Show a popup with a user-friendly error message
        showerror("Error", f"An unexpected error occurred:\n{str(e)}")

def create_gui():
    """
    Creates the main GUI window for the application.
    """
    root = Tk()
    root.title("Doc to PDF Converter")  # Set the title of the window

    # Add a label to the GUI
    Label(root, text="Doc to PDF Converter", font=("Helvetica", 16)).pack(pady=10)

    # Add a button for selecting and converting the file
    Button(
        root, text="Select and Convert File", command=run_converter, font=("Helvetica", 12), bg="blue", fg="white"
    ).pack(pady=20)

    # Add an exit button to close the application
    Button(root, text="Exit", command=root.quit, font=("Helvetica", 12), bg="red", fg="white").pack(pady=10)

    # Set the dimensions of the window
    root.geometry("400x200")

    # Start the GUI event loop
    root.mainloop()

# Run the GUI if this file is executed as a script
if __name__ == "__main__":
    create_gui()
