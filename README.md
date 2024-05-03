# PDF Editing Toolkit

## Description
This repository contains Python scripts for editing PDF files, particularly focusing on tasks like removing specific marks and resizing pages with bleeding. These scripts can be handy for individuals or businesses needing to manipulate PDF documents programmatically.

## Contents
1. **pdfwizard:** This directory contains scripts for modifying the content of PDF files.
   - **mirrorer.py:** PDFMirrorer allow mirroring a pdf on vertical, horizontal or both axes using PyPDF.
   - **redactor.py:** PDFRedactor removes specific marks from PDF documents using PyMuPDF (fitz).
   - **scaler.py:** PDFScaler modify the page size of every page of the pdf using PyMuPDF (fitz).
   - **bleeder.py:** PDFBleeder adds the bleed margin to the pdf.
   
2. **main.py:** This script is an example implementation demonstrating how to utilize the functionality provided by the pdfwizard scripts to edit PDF files.

## Usage
- Ensure you have Python installed on your system.
- Install the required dependencies listed in the `requirements.txt` file using pip.
- Place the PDF file you want to edit in the same directory as the scripts.
- Modify the `main.py` script according to your requirements, specifying the input PDF file name, the mark to remove (if using PDFRedactor), the desired page size (if using PDFScaler), and bleeding value (if using PDFBleeder).
- Run the `main.py` script, which will process the input PDF file according to the specified modifications and generate an output PDF file.

## Dependencies
- PyMuPDF
- PyPDF
- tqdm

## Note
These scripts are intended for automated or batch processing of PDF files. Ensure that you have the necessary permissions to modify the PDF files and that you understand the implications of the transformations being applied. Always make backups of important files before performing any modifications.
