from pdfwizard import PDFBleeder, PDFRedactor, PDFScaler


with open("input.pdf", "rb") as file:
    pdf_content = file.read()

needle = "e Paolo Palumbo"
size = 'Letter'
bleed = 9

original_content = pdf_content
scaler = PDFScaler(pdf_content)
pdf_content = scaler.scale(size)

bleeder = PDFBleeder(pdf_content, original_content)
pdf_content = bleeder.bleeding(bleed)

redactor = PDFRedactor(pdf_content)
pdf_content = redactor.remove_mark(needle)

with open("out.pdf", "wb") as output_file:
    output_file.write(pdf_content)


