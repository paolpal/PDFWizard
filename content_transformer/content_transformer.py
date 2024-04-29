import io
from tqdm import tqdm
import fitz

def remove_mark(input_stream, needle):
    # Carica il byte stream in un documento PDF utilizzando PyMuPDF (fitz)
    doc = fitz.open(stream=input_stream, filetype="pdf")

    # Itera su tutte le pagine del documento
    for page in tqdm(doc, desc="Searching the Needle"):
        # Cerca la posizione del testo su questa pagina
        draft = page.search_for(needle, quads=True)

        # Itera su tutti i quads trovati sulla pagina
        for rect in draft:
            # Aggiunge un'annotazione di redazione per ciascun quad trovato
            annot = page.add_redact_annot(rect)

        # Applica le redazioni
        page.apply_redactions(images=3)

    # Salva il nuovo PDF in un buffer di byte
    output_buffer = io.BytesIO()
    doc.save(output_buffer, garbage=3, deflate=True)

    # Chiude il documento PDF
    doc.close()

    # Resetta il cursore del buffer e restituisce il byte stream del PDF modificato
    output_buffer.seek(0)
    return output_buffer.getvalue()
