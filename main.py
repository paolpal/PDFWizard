import page_transformer.page_transformer as pt
import content_transformer.content_transformer as ct

with open("example.pdf", "rb") as file:
    pdf_content = file.read()

needle = "Paolo Palumbo"
pdf_content = ct.remove_mark(pdf_content, needle)


size = 'Letter'
bleed = 9
pdf_content = pt.bleed_and_resize(pdf_content, size, bleed)

with open("output.pdf", "wb") as output_file:
    output_file.write(pdf_content)