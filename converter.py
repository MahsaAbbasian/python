import os
from docx import Document
from reportlab.pdfgen import canvas
import tkinter as tk
from tkinter import filedialog

def convert_doc_to_pdf(input_path, output_path):
    try:
        #open .doc file
        doc = Document(input_path)
        #create new pdf file
        pdf = canvas.Canvas(output_path)
        #stating y position in the pdf file
        y_position = 800

        #loop through the paragraph in .doc file inorder to create a new pdf
        for paragraph in doc.paragraphs:
            # Write each paragraph's text on the PDF canvas
            pdf.drawString(100, y_position, paragraph.text)
            #moveing down size
            y_position -=20

        pdf.save()
        return True, f"File converted successfully and saved to: {output_path} "
    except Exception as e:
        return False,str(e)