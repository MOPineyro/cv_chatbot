from pinecone import Pinecone
from typing import List, Dict
from config import (
    PINECONE_API_KEY,
    PINECONE_INDEX_NAME
)
from embeddings import EmbeddingGenerator
from langchain.vectorstores import Pinecone as LangchainPinecone
from langchain.embeddings import OpenAIEmbeddings

class VectorStore:
    def __init__(self):
        self.pc = Pinecone(api_key=PINECONE_API_KEY)
        self.index = self.pc.Index(PINECONE_INDEX_NAME)
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        self.vectorstore = None
        self.initialize_vectorstore()

    def initialize_vectorstore(self):
        """Inicializar el vectorstore de Langchain"""
        self.vectorstore = LangchainPinecone.from_existing_index(
            index_name=PINECONE_INDEX_NAME,
            embedding=self.embeddings,
            text_key="text"
        )

    def get_retriever(self):
        """Obtener el retriever de Langchain"""
        return self.vectorstore.as_retriever()

    def add_texts(self, texts: List[str], metadata: List[Dict] = None) -> List[str]:
        """Agrega textos al almacén vectorial con metadatos opcionales"""
        try:
            # Debug print
            print("\nTextos a procesar:")
            for text in texts:
                print(f"- {text[:100]}...")

            # Usar el vectorstore de Langchain para agregar textos
            ids = self.vectorstore.add_texts(
                texts=texts,
                metadatas=[{"text": text, **(m if m else {})} for text, m in zip(texts, metadata if metadata else [None]*len(texts))]
            )
            
            print(f"\nVectores insertados: {len(ids)}")
            return ids
        
        except Exception as e:
            print(f"Error al agregar textos al almacén vectorial: {str(e)}")
            raise

    def similarity_search(self, query: str, k: int = 3) -> List[Dict]:
        """Busca textos similares usando una consulta"""
        try:
            # Debug print
            print(f"\nProcesando consulta: {query}")
            
            # Usar el vectorstore de Langchain para búsqueda
            docs = self.vectorstore.similarity_search_with_score(query, k=k)
            
            # Debug print
            print(f"Resultados encontrados: {len(docs)}")
            
            # Formatear resultados
            matches = []
            for doc, score in docs:
                matches.append({
                    'text': doc.page_content,
                    'score': score,
                    **doc.metadata
                })
            
            return matches
        
        except Exception as e:
            print(f"Error al realizar la búsqueda por similitud: {str(e)}")
            raise