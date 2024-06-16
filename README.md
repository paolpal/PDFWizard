# PDF Editing Toolkit

## Description
This repository contains Python scripts for editing PDF files, particularly focusing on tasks like removing specific marks and resizing pages with bleeding. These scripts can be handy for individuals or businesses needing to manipulate PDF documents programmatically.

## Contents
1. **pdfwizard:** This directory contains scripts for modifying the content of PDF files.
   - **mirrorer.py:** PDFMirrorer allow mirroring a pdf on vertical, horizontal or both axes using PyPDF.
   - **redactor.py:** PDFRedactor removes specific marks from PDF documents using PyMuPDF (fitz).
   - **scaler.py:** PDFScaler modify the page size of every page of the pdf using PyMuPDF (fitz).
   - **bleeder.py:** PDFBleeder adds the bleed margin to the pdf.
   
2. **main.py:** This script serves as a program that exposes the functionalities provided by the pdfwizard scripts for editing PDF files. It demonstrates how to utilize these functionalities effectively.

## Installation

```sh
git clone https://github.com/your-username/PDFWizard.git
cd PDFWizard
pip install .
```

### Uninstall
To uninstall PDFWizard, run:

```sh
pip uninstall pdfwizard
```

## Usage

To use the PDF transformation tool, run the script `main.py` with the following command-line arguments:

```bash
pdfwizard -i input.pdf -o output.pdf -n "string_to_remove" -s Letter -b 9 --no-bleed
```

### Command-line arguments:
- `-i, --input`: Specify the input PDF file.
- `-o, --output`: Specify the output PDF file (default: out.pdf if not specified).
- `-n, --needle`: Optional. Specify a string to remove from the PDF pages.
- `-s, --size`: Optional. Specify the page size for resizing the PDF (Letter, Legal, etc.).
- `-b, --bleed`: Optional. Specify the bleed value for PDF pages (default: 0).
- `--no-bleed`: Optional flag. Disable bleeding for PDF pages.

### Examples
1. Resize a PDF to A4 size:

```bash
pdfwizard -i input.pdf -s A4
```
2. Remove a watermark from a PDF:

```bash
pdfwizard -i input.pdf -n "Confidential"
```
3. Apply bleeding and resize a PDF:

```bash
pdfwizard -i input.pdf -s A4 -b 5
```

### Notes:
At least one of -n, -s, or -b must be provided for the tool to perform any action.
If -o is not specified, the output PDF will default to out.pdf.
Ensure all paths to PDF files are correctly specified.

## Dependencies
- PyMuPDF
- PyPDF
- tqdm

## Note
These scripts are intended for automated or batch processing of PDF files. Ensure that you have the necessary permissions to modify the PDF files and that you understand the implications of the transformations being applied. Always make backups of important files before performing any modifications.
