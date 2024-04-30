# PDF Editing Toolkit

## Description
This repository contains Python scripts for editing PDF files, particularly focusing on tasks like removing specific marks and resizing pages with bleeding. These scripts can be handy for individuals or businesses needing to manipulate PDF documents programmatically.

## Contents
1. **content_transformer:** This directory contains scripts for modifying the content of PDF files.
   - **content_transformer.py:** This script removes specific marks from PDF documents using PyMuPDF (fitz).
   
2. **page_transformer:** This directory includes scripts for transforming the pages of PDF files.
   - **page_transformer.py:** This script resizes PDF pages with bleeding to a specified size.
   
3. **main.py:** This script is an example implementation demonstrating how to utilize the functionality provided by the content_transformer and page_transformer scripts to edit PDF files.

## Usage
- Ensure you have Python installed on your system.
- Install the required dependencies listed in the `requirements.txt` file using pip.
- Place the PDF file you want to edit in the same directory as the scripts.
- Modify the `main.py` script according to your requirements, specifying the input PDF file name, the mark to remove (if using content_transformer), the desired page size, and bleeding value (if using page_transformer).
- Run the `main.py` script, which will process the input PDF file according to the specified modifications and generate an output PDF file.

## Dependencies
- PyMuPDF
- PyPDF2
- tqdm

## Note
These scripts are intended for automated or batch processing of PDF files. Ensure that you have the necessary permissions to modify the PDF files and that you understand the implications of the transformations being applied. Always make backups of important files before performing any modifications.
