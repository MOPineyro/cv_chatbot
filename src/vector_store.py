from pinecone import Pinecone
from typing import List, Dict
from config import (
    PINECONE_API_KEY,
    PINECONE_INDEX_NAME
)
from embeddings import EmbeddingGenerator
from langchain_community.vectorstores import Pinecone as LangchainPinecone
from langchain_openai import OpenAIEmbeddings

class VectorStore:
    def __init__(self, namespace: str = "default"):
        """Inicializar el almacén vectorial"""
        self.pc = Pinecone(api_key=PINECONE_API_KEY)
        self.index = self.pc.Index(PINECONE_INDEX_NAME)
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        self.namespace = namespace
        self.vectorstore = None
        self.initialize_vectorstore()

    def initialize_vectorstore(self):
        """Inicializar el vectorstore de Langchain"""
        try:
            # Crear vectorstore con el namespace especificado
            self.vectorstore = LangchainPinecone(
                embedding=self.embeddings,
                index=self.index,
                text_key="text",
                namespace=self.namespace
            )
            print(f"Vectorstore inicializado en namespace: {self.namespace}")
        except Exception as e:
            print(f"Error inicializando vectorstore: {str(e)}")
            raise

    def get_retriever(self):
        """Obtener el retriever de Langchain"""
        return self.vectorstore.as_retriever()

    def add_texts(self, texts: List[str], metadata: List[Dict] = None) -> List[str]:
        """Agrega textos al almacén vectorial con metadatos opcionales"""
        try:
            print(f"\nAgregando textos al namespace: {self.namespace}")
            print(f"Número de textos a agregar: {len(texts)}")
            
            # Preparar metadatos con namespace
            metadatas = []
            for i, text in enumerate(texts):
                meta = {"text": text, "namespace": self.namespace}
                if metadata and i < len(metadata) and metadata[i]:
                    meta.update(metadata[i])
                metadatas.append(meta)
            
            # Agregar textos al vectorstore
            ids = self.vectorstore.add_texts(
                texts=texts,
                metadatas=metadatas,
                namespace=self.namespace  # Especificar namespace explícitamente
            )
            
            # Verificar inserción
            stats = self.index.describe_index_stats()
            print(f"Estado del índice después de inserción: {stats}")
            
            # Mostrar stats específicos del namespace
            namespace_stats = stats.get('namespaces', {}).get(self.namespace, {})
            print(f"Vectores en namespace {self.namespace}: {namespace_stats.get('vector_count', 0)}")
            
            return ids
        except Exception as e:
            print(f"Error al agregar textos al almacén vectorial: {str(e)}")
            raise

    def similarity_search(self, query: str, k: int = 3) -> List[Dict]:
        """Busca textos similares usando una consulta"""
        try:
            print(f"\nProcesando consulta: {query} en namespace: {self.namespace}")
            
            # Identificar tipo de consulta
            query_type = self._identify_query_type(query)
            print(f"Tipo de consulta identificado: {query_type}")
            
            # Ajustar búsqueda según tipo de consulta
            search_kwargs = {
                "k": k,
                "namespace": self.namespace,
                "filter": {"content_type": query_type} if query_type != 'general' else None
            }
            
            # Realizar búsqueda
            docs = self.vectorstore.similarity_search_with_score(query, **search_kwargs)
            
            print(f"Resultados encontrados: {len(docs)}")
            if len(docs) == 0:
                print("⚠️ Advertencia: No se encontraron resultados")
                # Intentar sin filtro si no hay resultados
                if query_type != 'general':
                    print("Reintentando búsqueda sin filtro de tipo...")
                    docs = self.vectorstore.similarity_search_with_score(
                        query, k=k, namespace=self.namespace
                    )
            
            for i, (doc, score) in enumerate(docs):
                print(f"\nResultado {i+1}: Score {score:.4f}")
                print(f"Sección: {doc.metadata.get('section', 'N/A')}")
                print(f"Tipo: {doc.metadata.get('content_type', 'N/A')}")
                print(f"Contenido: {doc.page_content[:200]}...")
            
            return [{"text": doc.page_content, "score": score, **doc.metadata} 
                    for doc, score in docs]
                
        except Exception as e:
            print(f"Error al realizar la búsqueda por similitud: {str(e)}")
            raise

    def _identify_query_type(self, query: str) -> str:
        """Identificar el tipo de consulta (español/inglés)"""
        query = query.lower()
        
        # Mapeo de tipos de consulta en ambos idiomas
        query_types = {
            'tecnologías': [
                # Español
                'tecnología', 'lenguaje', 'framework', 'herramienta', 'programa',
                'desarrollo', 'código', 'programación',
                # Inglés
                'technology', 'language', 'framework', 'tool', 'software',
                'development', 'code', 'programming'
            ],
            'educación': [
                # Español
                'educación', 'estudios', 'título', 'universidad', 'formación',
                'académico', 'carrera',
                # Inglés
                'education', 'studies', 'degree', 'university', 'academic',
                'school', 'college'
            ],
            'experiencia': [
                # Español
                'experiencia', 'trabajo', 'rol', 'puesto', 'cargo', 'empleo',
                'empresa', 'proyecto',
                # Inglés
                'experience', 'work', 'role', 'position', 'job', 'employment',
                'company', 'project'
            ],
            'habilidades': [
                # Español
                'habilidad', 'competencia', 'conocimiento', 'destreza', 'capacidad',
                # Inglés
                'skill', 'competency', 'knowledge', 'ability', 'expertise'
            ]
        }
        
        # Buscar coincidencias en cada tipo de consulta
        for query_type, keywords in query_types.items():
            if any(kw in query for kw in keywords):
                return query_type
                
        return 'general'