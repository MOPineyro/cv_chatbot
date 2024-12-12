from typing import List
import os
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter

class DocumentLoader:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )

    def load_pdf(self, file_path: str) -> List[str]:
        """Carga un archivo PDF y lo divide en chunks."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"No se encontró el archivo: {file_path}")
        
        try:
            pdf_reader = PdfReader(file_path)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            
            print(f"\nContenido extraído de {file_path}:")
            print(f"{text[:200]}...")
            
            # Dividir el texto en chunks
            chunks = self.text_splitter.split_text(text)
            
            print(f"Chunks generados: {len(chunks)}")
            for i, chunk in enumerate(chunks):
                print(f"\nChunk {i+1}:")
                print(f"{chunk[:100]}...")
            
            return chunks
        
        except Exception as e:
            print(f"Error al procesar el PDF: {str(e)}")
            raise

    def load_multiple_pdfs(self, directory: str) -> dict:
        """Carga múltiples PDFs desde un directorio."""
        documents = {}
        for filename in os.listdir(directory):
            if filename.endswith('.pdf'):
                file_path = os.path.join(directory, filename)
                documents[filename] = self.load_pdf(file_path)
        return documents 