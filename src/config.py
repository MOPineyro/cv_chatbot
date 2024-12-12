import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de APIs
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Configuración del modelo
EMBEDDING_MODEL_NAME = "text-embedding-3-small"  # Modelo de OpenAI para embeddings
LLM_MODEL_NAME = "mixtral-8x7b-32768"  # Modelo de Groq para generación de texto

# Configuración de Pinecone
PINECONE_INDEX_NAME = "cv-embeddings"
PINECONE_DIMENSION = 1536  # Dimensión para text-embedding-3-small

# Configuración de la aplicación
MAX_TOKENS = 4096
TEMPERATURE = 0.7 