import io
from tqdm import tqdm
import pypdf

class PDFMirrorer:
	def __init__(self, input_stream):
		self.input_stream = input_stream

	def mirror_horizontally(self):
		return self._mirror_pages(True, False)

	def mirror_vertically(self):
		return self._mirror_pages(False, True)

	def mirror_both(self):
		return self._mirror_pages(True, True)

	def _mirror_pages(self, horizontal, vertical):
		input_pdf = io.BytesIO(self.input_stream)
		reader = pypdf.PdfReader(input_pdf)
		writer = pypdf.PdfWriter()

		mirror_direction = "horizontal" if horizontal else "vertical"
		mirror_direction = "both" if horizontal and vertical else mirror_direction
		desc = f"Mirroring ({mirror_direction})"

		for	page in tqdm(reader.pages, desc=desc):
			mirrored_page = self._mirror_page(page, horizontal, vertical)
			writer.add_page(mirrored_page)

		output_pdf = io.BytesIO()
		writer.write(output_pdf)
		return output_pdf.getvalue()

	@staticmethod
	def _mirror_page(page, horizontal, vertical):
		mirrored_page = page
		scale_x = -1 if horizontal else 1
		scale_y = -1 if vertical else 1
		mirrored_page.scale(scale_x, scale_y)
		return mirrored_page

# Utilizzo della classe PDFMirror
#with open("input.pdf", "rb") as input_file:
#	input_stream = input_file.read()

#pdf_mirror = PDFMirror(input_stream)

# Specchiamento orizzontale
#output_stream_horizontal = pdf_mirror.mirror_horizontally()

# Specchiamento verticale
#output_stream_vertical = pdf_mirror.mirror_vertically()

# Specchiamento sia orizzontale che verticale
#output_stream_both = pdf_mirror.mirror_both()

# Scrivere gli output_stream in file o utilizzarli come richiesto
