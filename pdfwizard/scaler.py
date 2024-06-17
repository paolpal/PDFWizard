import fitz
import json
import io
import os
from tqdm import tqdm

class PDFScaler:
	page_sizes = {
		"Letter": [612, 792],
		"Legal": [612, 1008],
		"Ledger": [792, 1224],
		"Tabloid": [1224, 792],
		"A0": [2384, 3370],
		"A1": [1684, 2384],
		"A2": [1190, 1684],
		"A3": [842, 1190],
		"A4": [595, 842],
		"A5": [420, 595],
		"A6": [298, 420],
		"A7": [210, 298],
		"A8": [148, 210]
	}

	def __init__(self, input_stream):
		self.input_stream = input_stream
		self.page_sizes = {
			"Letter": [612, 792],
			"Legal": [612, 1008],
			"Ledger": [792, 1224],
			"Tabloid": [1224, 792],
			"A0": [2384, 3370],
			"A1": [1684, 2384],
			"A2": [1190, 1684],
			"A3": [842, 1190],
			"A4": [595, 842],
			"A5": [420, 595],
			"A6": [298, 420],
			"A7": [210, 298],
			"A8": [148, 210]
		}


	def scale(self, size):
		if size not in PDFScaler.page_sizes:
			raise ValueError(f"Invalid size '{size}'. Valid sizes are: {', '.join(self.page_sizes.keys())}")
		# Crea un nuovo documento vuoto
		scaled_document = fitz.open()
		target_width, target_height = PDFScaler.page_sizes[size]
		# Apri il documento PDF di input
		document = fitz.open(stream=self.input_stream, filetype="pdf")

		# Itera attraverso le pagine del documento di input
		for page in tqdm(document, desc="Scaling"):
			
			width = page.rect.width
			height = page.rect.height

			ratio = min(target_width/width, target_height/height)
			self.dx = abs(ratio*width-target_width)/2
			self.dy = abs(ratio*height-target_height)/2


			# Applica lo scaling alla pagina corrente
			scaled_page = scaled_document.new_page(-1,
						width = target_width,
						height = target_height)

			scaled_rect = scaled_page.rect + fitz.Rect(self.dx,self.dy,-self.dx,-self.dy)

			scaled_page.show_pdf_page(
				scaled_rect, 
				document,  # input document
				page.number,  # input page number
			)

		# Chiudi il documento di input
		document.close()

		output_stream = io.BytesIO()
		scaled_document.save(output_stream)
		output_stream.seek(0)

		return output_stream.getvalue()
