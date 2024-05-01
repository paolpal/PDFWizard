from pdfwizard import PDFMirrorer, PDFRotator, PDFBleeder, PDFScaler, PDFRedactor


with open("fallout.pdf", "rb") as file:
    pdf_content = file.read()

needle = "Giacomo Arcuri - 295268"
size = 'Letter'
bleed = 9

mirrorer = PDFMirrorer(pdf_content)
rotator = PDFRotator(pdf_content)
scaler = PDFScaler(pdf_content)

pdf_vertical = mirrorer.mirror_vertically()
pdf_horizontal = mirrorer.mirror_horizontally()
pdf_both = mirrorer.mirror_both()

#pdf_content = scaler.scale(size)
#ratio = scaler.get_ratio()

# Combina i documenti e ottiene lo stream del documento combinato
bleeder = PDFBleeder(pdf_content, pdf_vertical, pdf_horizontal, pdf_both)
pdf_content = bleeder.bleeding(bleed)

redactor = PDFRedactor()

pdf_content = redactor.remove_mark(pdf_content, needle)

with open("out.pdf", "wb") as output_file:
    output_file.write(pdf_content)


