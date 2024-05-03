import io
from tqdm import tqdm
import pypdf

class PDFRotator:
	def __init__(self, input_stream):
		self.input_stream = input_stream

	def rotate_pages(self, angle=180):
		input_pdf = io.BytesIO(self.input_stream)
		reader = pypdf.PdfReader(input_pdf)
		writer = pypdf.PdfWriter()

		for	page in tqdm(reader.pages, desc="Rotating"):
			rotated_page = page.rotate(angle)
			writer.add_page(rotated_page)

		output_pdf = io.BytesIO()
		writer.write(output_pdf)
		return output_pdf.getvalue()