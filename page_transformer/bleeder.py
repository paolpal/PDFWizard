import fitz
from tqdm import tqdm
import io

class PDFBleeder:
    def __init__(self, document_stream, v_mirrored_stream, h_mirrored_stream, b_mirrored_stream):
        self.document_stream = document_stream
        self.v_mirrored_stream = v_mirrored_stream
        self.h_mirrored_stream = h_mirrored_stream
        self.b_mirrored_stream = b_mirrored_stream

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
            width = page.rect.width
            height = page.rect.height

            combined_page = combined_document.new_page(-1,
                           width = width + 2*bleed,
                           height = height + 2*bleed)

            #for doc in [document, v_mirrored, h_mirrored, b_mirrored]:
            combined_page.show_pdf_page(
                page.rect+bleed, 
                document,  # input document
                page.number,  # input page number
            )

            # left bleed
            dest = fitz.Rect(0, bleed, bleed, height+bleed)
            clip = fitz.Rect(width-bleed, 0, width, height)

            combined_page.show_pdf_page(
                dest, 
                h_mirrored,  # input document
                page.number,  # input page number
                clip=clip,
            )

            # right bleed
            dest = fitz.Rect(width+bleed, bleed, width+2*bleed, height+bleed)
            clip = fitz.Rect(0, 0, bleed, height)

            combined_page.show_pdf_page(
                dest, 
                h_mirrored,  # input document
                page.number,  # input page number
                clip=clip,
            )

            # top bleed
            dest = fitz.Rect(bleed, 0, width+bleed, bleed)
            clip = fitz.Rect(0, height-bleed, width, height)

            combined_page.show_pdf_page(
                dest, 
                v_mirrored,  # input document
                page.number,  # input page number
                clip=clip,
            )

            # bottom bleed
            dest = fitz.Rect(bleed, height+bleed, width+bleed, height+2*bleed)
            clip = fitz.Rect(0, 0, width, bleed)

            combined_page.show_pdf_page(
                dest, 
                v_mirrored,  # input document
                page.number,  # input page number
                clip=clip,
            )

            # Corners
            # Top Left bleed
            dest = fitz.Rect(0, 0, bleed, bleed)
            clip = fitz.Rect(width-bleed, height-bleed, width, height)

            combined_page.show_pdf_page(
                dest, 
                b_mirrored,  # input document
                page.number,  # input page number
                clip=clip,
            )

            # Bottom Right bleed
            dest = fitz.Rect(width+bleed, height+bleed, width+2*bleed, height+2*bleed)
            clip = fitz.Rect(0, 0, bleed, bleed)

            combined_page.show_pdf_page(
                dest, 
                b_mirrored,  # input document
                page.number,  # input page number
                clip=clip,
            )

            # Top Right bleed
            dest = fitz.Rect(width+bleed, 0, width+2*bleed, bleed)
            clip = fitz.Rect(0, height-bleed, bleed, height)

            combined_page.show_pdf_page(
                dest, 
                b_mirrored,  # input document
                page.number,  # input page number
                clip=clip,
            )

            # Bottom Left bleed
            dest = fitz.Rect(0, height+bleed, bleed, height+2*bleed)
            clip = fitz.Rect(width-bleed, 0, width, bleed)

            combined_page.show_pdf_page(
                dest, 
                b_mirrored,  # input document
                page.number,  # input page number
                clip=clip,
            )

        # Ottieni lo stream del documento combinato
        output_stream = io.BytesIO()
        combined_document.save(output_stream)
        output_stream.seek(0)

        return output_stream.getvalue()

# Utilizzo della classe Bleeder
if __name__ == "__main__":
    # Esempio di stream di documenti PDF
    document_stream = b'...'  # Stream del documento originale
    v_mirrored_stream = b'...'  # Stream del documento con mirror verticale
    h_mirrored_stream = b'...'  # Stream del documento con mirror orizzontale
    b_mirrored_stream = b'...'  # Stream del documento con mirror su entrambi gli assi

    # Creazione dell'istanza della classe Bleeder
    bleeder = Bleeder(document_stream, v_mirrored_stream, h_mirrored_stream, b_mirrored_stream)

    # Combina i documenti e ottiene lo stream del documento combinato
    combined_document_stream = bleeder.combine_documents()

    # Ora puoi utilizzare combined_document_stream come desideri
