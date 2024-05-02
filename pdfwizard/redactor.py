import io
from tqdm import tqdm
import fitz

class PDFRedactor:
    """
    Classe per la rimozione di testo da PDF.

    Utilizza PyMuPDF (fitz) per cercare e rimuovere testo all'interno di un file PDF.

    Esempi di utilizzo:

    >>> redactor = PDFRedactor()
    >>> with open('input.pdf', 'rb') as input_stream:
    >>>     redacted_pdf = redactor.remove_mark(input_stream, "testo da rimuovere")
    >>> with open('output.pdf', 'wb') as output_stream:
    >>>     output_stream.write(redacted_pdf)
    """

    def __init__(self):
        pass

    def remove_mark(self, input_stream, needle):
        """
        Rimuove il testo specificato da un PDF.

        Parametri:
            input_stream (bytes): Stream di input del file PDF.
            needle (str): Testo da cercare e rimuovere.

        Restituisce:
            bytes: Stream di output del PDF redatto.
        """

        # Carica il byte stream in un documento PDF utilizzando PyMuPDF (fitz)
        doc = fitz.open(stream=input_stream, filetype="pdf")

        # Itera su tutte le pagine del documento
        for page in tqdm(doc, desc="Ricerca del testo"):
            # Cerca la posizione del testo su questa pagina
            draft = page.search_for(needle, quads=True)

            # Itera su tutti i quads trovati sulla pagina
            for rect in draft:
                # Aggiunge un'annotazione di redazione per ciascun quad trovato
                annot = page.add_redact_annot(rect-2) # STRANO FIX PER UN CASO
                # il -2 non so cosa faccia, ma corregge il problema che riscontravo. Potrebbe non servire sempre.

            # Applica le redazioni
            page.apply_redactions(images=3)

        # Salva il nuovo PDF in un buffer di byte
        output_buffer = io.BytesIO()
        doc.save(output_buffer)

        # Chiude il documento PDF
        doc.close()

        # Resetta il cursore del buffer e restituisce il byte stream del PDF modificato
        output_buffer.seek(0)
        return output_buffer.getvalue()
