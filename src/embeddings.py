from openai import OpenAI
from typing import List
import numpy as np
from config import OPENAI_API_KEY

class EmbeddingGenerator:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.model = "text-embedding-3-small"

    def generate_embeddings(self, texts: List[str]) -> List[np.ndarray]:
        """Genera embeddings usando el modelo de OpenAI."""
        try:
            response = self.client.embeddings.create(
                model=self.model,
                input=texts,
                encoding_format="float"
            )
            # Extraer los embeddings de la respuesta
            embeddings = [embedding.embedding for embedding in response.data]
            return embeddings
            
        except Exception as e:
            print(f"Error al generar embeddings: {str(e)}")
            raise 