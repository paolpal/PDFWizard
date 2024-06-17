import argparse
from . import PDFBleeder, PDFRedactor, PDFScaler

def process_pdf(input_path, output_path, needle=None, size=None, bleed=0, no_bleed=False):
    with open(input_path, "rb") as file:
        pdf_content = file.read()

    original_content = pdf_content

    if size:
        scaler = PDFScaler(pdf_content)
        pdf_content = scaler.scale(size)

    if not no_bleed:
        bleeder = PDFBleeder(pdf_content, original_content)
        pdf_content = bleeder.bleeding(bleed)

    if needle:
        redactor = PDFRedactor(pdf_content)
        pdf_content = redactor.remove_mark(needle)

    with open(output_path, "wb") as output_file:
        output_file.write(pdf_content)


def main():
    parser = argparse.ArgumentParser(description="Tool for processing PDF files.")
    parser.add_argument('-i', '--input', type=str, required=True, help='Input PDF file path')
    parser.add_argument('-o', '--output', type=str, default='out.pdf', help='Output PDF file path (default: out.pdf)')
    parser.add_argument('-n', '--needle', type=str, help="String to remove from the PDF")
    parser.add_argument('-s', '--size', type=str, help="Size for resizing the PDF (e.g., 'Letter')")
    parser.add_argument('-b', '--bleed', type=int, default=0, help="Bleeding value for the PDF (default: 0)")
    parser.add_argument('--no-bleed', action='store_true', help="Disable bleeding")

    args = parser.parse_args()

    # Controlli logici usando argparse
    if args.bleed and args.no_bleed:
        parser.error("Cannot specify both --bleed and --no-bleed simultaneously.")

    if not (args.needle or args.size or args.bleed):
        parser.error("At least one of --needle, --size, or --bleed must be specified.")

    if args.size is not None and args.size not in PDFScaler.page_sizes.keys():
        parser.error(f"Invalid size '{args.size}'. Valid sizes are: {', '.join(PDFScaler.page_sizes.keys())}")

    try:
        process_pdf(args.input, args.output, args.needle, args.size, args.bleed, args.no_bleed)
    except ValueError as e:
        parser.print_help()
        parser.error(f"{e}")

if __name__ == '__main__':
    main()