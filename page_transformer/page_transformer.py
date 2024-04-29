import PyPDF2
import copy
from tqdm import tqdm
import io

# Dimensioni standard delle pagine in punti
PAGE_SIZES = {
	'Letter': (612, 792),
	'Legal': (612, 1008),
	'Ledger': (792, 1224),
	'Tabloid': (1224, 792),
	'A0': (2384, 3370),
	'A1': (1684, 2384),
	'A2': (1190, 1684),
	'A3': (842, 1190),
	'A4': (595, 842),
	'A5': (420, 595),
	'A6': (298, 420),
	'A7': (210, 298),
	'A8': (148, 210),
}

def new_page(width, height):
	page = PyPDF2._page.PageObject.create_blank_page(None, width, height)
	return page

def resize(page, width, height, size, bleed):
	target_width, target_height = PAGE_SIZES[size]
	new_width = target_width + 2 * bleed
	new_height = target_height + 2 * bleed

	ratio = min(target_width/width, target_height/height)
	new = new_page(new_width,new_height)
	new.merge_page(page)

	dx = abs(ratio*width-target_width)
	dy = abs(ratio*height-target_height)
	new.add_transformation((ratio, 0, 0, ratio, bleed+(dx/2), bleed+(dy/2)))
	
	return new, ratio

def modify(page, width, height, size, bleed):
	target_width, target_height = PAGE_SIZES[size]
	new_width = target_width + 2 * bleed
	new_height = target_height + 2 * bleed

	new, ratio = resize(page, width, height, size, bleed)
	dx = abs(ratio*width-target_width)
	dy = abs(ratio*height-target_height)
	
	actual_width = ratio*width
	actual_height = ratio*height

	wbleed = bleed + dx/2
	hbleed = bleed + dy/2

	transformations = [
		(-ratio, 0, 0, ratio, wbleed, hbleed), # left
		(-ratio, 0, 0, -ratio, wbleed, hbleed), # bottom left 
		(ratio, 0, 0, -ratio, wbleed, hbleed), # bottom
		(-ratio, 0, 0, -ratio, 2 * actual_width + wbleed, hbleed), # bottom right
		(-ratio, 0, 0, ratio, 2 * actual_width + wbleed, hbleed), # right
		(ratio, 0, 0, -ratio, wbleed, 2 * actual_height + hbleed), # top
		(-ratio, 0, 0, -ratio, wbleed, 2 * actual_height + hbleed), # top left
		(-ratio, 0, 0, -ratio, 2 * actual_width + wbleed, 2 * actual_height + hbleed), # top right
	]

	bleed_template = new_page(new_width, new_height)
	bleed_template.merge_page(page)
	bleed_template.compress_content_streams()

	for transformation in transformations:
		new_bleed = copy.copy(bleed_template)
		new_bleed.add_transformation(transformation)
		new.merge_page(new_bleed)
		del new_bleed
	
	return new

def bleed_and_resize(input_content, size, bleed):
	reader = PyPDF2.PdfReader(io.BytesIO(input_content))
	writer = PyPDF2.PdfWriter()
	output = io.BytesIO()
	
	for page in tqdm((reader.pages), desc="Editing Pages"):
		width = page.mediabox.width
		height = page.mediabox.height
		new = modify(page, width, height, size, bleed)
		writer.add_page(new)
		del new

	writer.write(output)
	return output.getvalue()

