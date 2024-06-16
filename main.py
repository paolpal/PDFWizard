import argparse
from pdfwizard import PDFBleeder, PDFRedactor, PDFScaler

def main(input_path, output_path, needle=None, size=None, bleed=0, no_bleed=False):
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


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Tool per il processing di PDF.")
    parser.add_argument('-i', '--input', type=str, required=True, help='Percorso del file PDF di input')
    parser.add_argument('-o', '--output', type=str, default='out.pdf', help='Percorso del file PDF di output (default: out.pdf)')
    parser.add_argument('-n', '--needle', type=str, help="Stringa da rimuovere dal PDF")
    parser.add_argument('-s', '--size', type=str, help="Dimensione per il ridimensionamento del PDF (ad esempio, 'Letter')")
    parser.add_argument('-b', '--bleed', type=int, default=0, help="Valore di bleeding per il PDF (default: 0)")
    parser.add_argument('--no-bleed', action='store_true', help="Disabilita il bleeding")

    args = parser.parse_args()

    # Controlli logici usando argparse
    if args.bleed and args.no_bleed:
        parser.error("Non è possibile specificare contemporaneamente --bleed e --no-bleed.")

    if not (args.needle or args.size or args.bleed):
        parser.error("Deve essere specificato almeno uno tra --needle, --size, o --bleed.")

    try:
        main(args.input, args.output, args.needle, args.size, args.bleed, args.no_bleed)
    except ValueError as e:
        print(f"Errore: {e}")
        parser.print_help()
