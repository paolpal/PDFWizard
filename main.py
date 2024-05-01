import page_transformer.page_transformer as pt
import content_transformer.content_transformer as ct
from page_transformer import PDFMirrorer, PDFRotator, PDFBleeder


with open("dark.pdf", "rb") as file:
    pdf_content = file.read()

needle = "Paolo Palumbo"
#pdf_content = ct.remove_mark(pdf_content, needle)

mirrorer = PDFMirrorer(pdf_content)
rotator = PDFRotator(pdf_content)

pdf_vertical = mirrorer.mirror_vertically()
pdf_horizontal = mirrorer.mirror_horizontally()
pdf_both = mirrorer.mirror_both()

size = 'Letter'
bleed = 9

with open("both.pdf", "wb") as output_file:
    output_file.write(pdf_both)

#pdf_content = pt.bleed_and_resize(pdf_content, size, bleed)
#pdf_content = pageTransormer.bleed_and_resize(pdf_content, size, bleed)

# Combina i documenti e ottiene lo stream del documento combinato
bleeder = PDFBleeder(pdf_content, pdf_vertical, pdf_horizontal, pdf_both)
pdf_content = bleeder.bleeding(bleed)


with open("out.pdf", "wb") as output_file:
    output_file.write(pdf_content)


