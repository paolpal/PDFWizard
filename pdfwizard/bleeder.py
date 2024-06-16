import fitz
from tqdm import tqdm
import io
from pdfwizard.mirrorer import PDFMirrorer

class PDFBleeder:
	# usa il mirrorer direttamente dentro alla classe
	# passa solo il documento originale
	def __init__(self, document_stream, original_stream=None):
		self.document_stream = document_stream
		if original_stream is None:
			original_stream = document_stream
		mirrorer = PDFMirrorer(original_stream)
		self.v_mirrored_stream = mirrorer.mirror_vertically()
		self.h_mirrored_stream = mirrorer.mirror_horizontally()
		self.b_mirrored_stream = mirrorer.mirror_both()

	def create_document(self, stream):
		return fitz.open(stream=stream, filetype="pdf")

	def bleeding(self, bleed):
		# Crea i documenti da ogni stream
		document = self.create_document(self.document_stream)
		v_mirrored = self.create_document(self.v_mirrored_stream)
		h_mirrored = self.create_document(self.h_mirrored_stream)
		b_mirrored = self.create_document(self.b_mirrored_stream)

		# Crea il documento combinato
		combined_document = fitz.open()

		# Itera attraverso le pagine e unisci pagina per pagina
		for page in tqdm(document, desc="Bleeding"):
			target_width = page.rect.width
			target_height = page.rect.height

			original_width = h_mirrored[page.number].rect.width
			original_height = h_mirrored[page.number].rect.height

			ratio = min(target_width/original_width, target_height/original_height)
			
			dx = abs(ratio*original_width-target_width)/2
			dy = abs(ratio*original_height-target_height)/2
			
			actual_width = ratio*original_width
			actual_height = ratio*original_height

			w_bleed = bleed + dx
			h_bleed = bleed + dy

			combined_page = combined_document.new_page(-1,
						   width = target_width + 2*bleed,
						   height = target_height + 2*bleed)

			combined_page.show_pdf_page(
				page.rect + bleed, 
				document,  # input document
				page.number,  # input page number
			)

			bleed_transformations = [
				(fitz.Rect(0, h_bleed, w_bleed, actual_height+h_bleed), 
				fitz.Rect(original_width-(w_bleed/ratio), 0, original_width, original_height), 
				h_mirrored), # left bleed

				(fitz.Rect(actual_width+w_bleed, h_bleed, actual_width+2*w_bleed, actual_height+h_bleed), 
				fitz.Rect(0, 0, (w_bleed/ratio), original_height), 
				h_mirrored), # right bleed

				(fitz.Rect(w_bleed, 0, actual_width+w_bleed, h_bleed),
				fitz.Rect(0, original_height-(h_bleed/ratio), original_width, original_height),
				v_mirrored), # top bleed

				(fitz.Rect(w_bleed, actual_height+h_bleed, actual_width+w_bleed, actual_height+2*h_bleed),
				fitz.Rect(0, 0, original_width, (h_bleed/ratio)),
				v_mirrored), # bottom bleed

				(fitz.Rect(0, 0, w_bleed, h_bleed),
				fitz.Rect(original_width-(w_bleed/ratio), original_height-(h_bleed/ratio), original_width, original_height),
				b_mirrored), # Top Left bleed

				(fitz.Rect(actual_width+w_bleed, actual_height+h_bleed, actual_width+2*w_bleed, actual_height+2*h_bleed),
				fitz.Rect(0, 0, (w_bleed/ratio), (h_bleed/ratio)),
				b_mirrored), # Bottom Right bleed

				(fitz.Rect(actual_width+w_bleed, 0, actual_width+2*w_bleed, h_bleed),
				fitz.Rect(0, original_height-(h_bleed/ratio), (w_bleed/ratio), original_height),
				b_mirrored), # Top Right bleed

				# Bottom Left bleed
				(fitz.Rect(0, actual_height+h_bleed, w_bleed, actual_height+2*h_bleed),
				fitz.Rect(original_width-(w_bleed/ratio), 0, original_width, (h_bleed/ratio)),
				b_mirrored) # Bottom Left bleed

			]

			for dest, clip, doc in bleed_transformations:
				if not dest.is_empty and not clip.is_empty:
					combined_page.show_pdf_page(
						dest, 
						doc,  # input document
						page.number,  # input page number
						clip=clip,
					)

		# Ottieni lo stream del documento combinato
		output_stream = io.BytesIO()
		combined_document.save(output_stream, garbage=3, deflate=True)
		output_stream.seek(0)

		return output_stream.getvalue()

