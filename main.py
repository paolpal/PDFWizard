import page_transformer.page_transformer as pt
import content_transformer.content_transformer as ct
from page_transformer import PDFMirrorer, PDFRotator


with open("dark.pdf", "rb") as file:
    pdf_content = file.read()

needle = "Paolo Palumbo"
#pdf_content = ct.remove_mark(pdf_content, needle)

mirrorer = PDFMirrorer(pdf_content)
rotator = PDFRotator(pdf_content)

pdf_vertical = mirrorer.mirror_vertically()
pdf_horizontal = mirrorer.mirror_horizontally()
pdf_rotated = rotator.rotate_pages()

size = 'Letter'
bleed = 9
#pdf_content = pt.bleed_and_resize(pdf_content, size, bleed)

with open("vertical.pdf", "wb") as output_file:
    output_file.write(pdf_vertical)

with open("horizontal.pdf", "wb") as output_file:
    output_file.write(pdf_horizontal)

with open("both.pdf", "wb") as output_file:
    output_file.write(pdf_rotated)